from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import FeeType, FeePayment
from .forms import FeePaymentForm,FeeTypeForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import  A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and user.role in ['admin']

# List all fee payments
@login_required
@user_passes_test(is_admin)
def list_fee_payments(request):
    payments = FeePayment.objects.all()
    return render(request, 'fees/list_fee_payments.html', {'payments': payments})

# Create new fee payment
@login_required
@user_passes_test(is_admin)
def create_fee_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the fee payment, balance and status will be auto-calculated
            messages.success(request, 'Fee Payment added successfully!')
            return redirect('list_fee_payments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm()

    return render(request, 'fees/create_fee_payment.html', {'form': form})

# Edit fee payment
@login_required
@user_passes_test(is_admin)
def edit_fee_payment(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()  # This will automatically update the balance and status
            messages.success(request, 'Fee Payment updated successfully!')
            return redirect('list_fee_payments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm(instance=payment)

    return render(request, 'fees/edit_fee_payment.html', {'form': form})

# Delete fee payment
@login_required
@user_passes_test(is_admin)
def delete_fee_payment(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    payment.delete()
    messages.success(request, 'Fee Payment deleted successfully!')
    return redirect('list_fee_payments')



# List all fee types
@login_required
@user_passes_test(is_admin)
def list_fee_types(request):
    fee_types = FeeType.objects.all()
    return render(request, 'fees/list_fee_types.html', {'fee_types': fee_types})

# Create new fee type
@login_required
@user_passes_test(is_admin)
def create_fee_type(request):
    if request.method == 'POST':
        form = FeeTypeForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Fee Type added successfully!')
            return redirect('list_fee_types')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeePaymentForm()
    return render(request, 'fees/create_fee_type.html')

# Edit fee type
@login_required
@user_passes_test(is_admin)
def edit_fee_type(request, pk):
    fee_type = get_object_or_404(FeeType, pk=pk)
    if request.method == 'POST':
        
        if request.method == 'POST':
            form = FeeTypeForm(request.POST, instance=fee_type)
            if form.is_valid():
                form.save()  
                messages.success(request, 'Fee Type updated successfully!')
                return redirect('list_fee_types')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = FeeTypeForm(instance=fee_type)

    return render(request, 'fees/edit_fee_type.html', {'fee_type': fee_type})

# Delete fee type
@login_required
@user_passes_test(is_admin)
def delete_fee_type(request, pk):
    fee_type = get_object_or_404(FeeType, pk=pk)
    fee_type.delete()
    messages.success(request, 'Fee Type deleted successfully!')
    return redirect('list_fee_types')


@login_required
def generate_invoice_pdf(request, pk):
    # Get the FeePayment object
    payment = get_object_or_404(FeePayment, pk=pk)
    
    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    
    # Create a canvas (PDF document)
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Colors
    dark_color = colors.Color(0.1, 0.1, 0.1)
    light_gray = colors.Color(0.9, 0.9, 0.9)
    
    # Header Section
    # Add stylized logo/ampersand (if you have a logo, replace this section)
    logo_path = os.path.join(settings.MEDIA_ROOT, "logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 50, height - 120, width=80, height=80)
    else:
        # Fallback if logo doesn't exist
        p.setFont("Helvetica-Bold", 48)
        p.setFillColor(dark_color)
        p.drawString(50, height - 100, "&")

    # Organization details (bottom right)
    p.setFont("Helvetica-Bold", 25)
    p.setFillColor(dark_color)
    p.drawString(140, height - 80, "Sri Ganalaankra Maha Pirivena")
    
    p.setFont("Helvetica", 15)
    p.setFillColor(colors.black)
    p.drawString(140, height - 100, "Peradeniya, Sri Lanka")
    
    # Invoice title
    p.setFont("Helvetica-Bold", 36)
    p.setFillColor(dark_color)
    p.drawString(width - 200, height - 150, "INVOICE")
    
    # Invoice details (top right)
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    invoice_date = datetime.now().strftime("%d %B %Y")
    p.drawString(width - 200, height - 180, f"Invoice No. {payment.pk}")
    p.drawString(width - 200, height - 195, invoice_date)
    
    # Billed To Section
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.black)
    p.drawString(50, height - 180, "BILLED TO:")
    
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 200, payment.student.full_name)
    # Add phone and address if available in your model
    if hasattr(payment.student, 'telephone_number'):
        p.drawString(50, height - 215, f"+{payment.student.telephone_number}")
    if hasattr(payment.student, 'address'):
        p.drawString(50, height - 230, payment.student.address)
    

    
    # Table Section
    table_start_y = height - 300
    
    # Table header
    p.setFillColor(light_gray)
    p.rect(50, table_start_y - 25, width - 100, 25, fill=1, stroke=1)
    
    # Table header text
    p.setFont("Helvetica-Bold", 11)
    p.setFillColor(colors.black)
    p.drawString(70, table_start_y - 18, "Fee Type")
    p.drawString(330, table_start_y - 18, "Fee Amount")
    p.drawString(450, table_start_y - 18, "Paid Amount")
    
    # Table row
    row_y = table_start_y - 50
    p.setFont("Helvetica", 10)
    p.drawString(70, row_y, payment.fee_type.name)
    p.drawString(330, row_y, f"Rs {payment.fee_type.amount}")
    p.drawString(450, row_y, f"Rs {payment.paid_amount}")
    
    # Draw table borders
    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    
    # Horizontal lines
    p.line(50, table_start_y, width - 50, table_start_y)  # Top line
    p.line(50, table_start_y - 25, width - 50, table_start_y - 25)  # Header bottom
    p.line(50, row_y - 10, width - 50, row_y - 10)  # Row bottom
    
    # Vertical lines
    p.line(50, table_start_y, 50, row_y - 10)  # Left border
    p.line(320, table_start_y, 320, row_y - 10)  # Quantity column
    p.line(410, table_start_y, 410, row_y - 10)  # Unit Price column
    # p.line(490, table_start_y, 490, row_y - 10)  # Total column
    p.line(width - 50, table_start_y, width - 50, row_y - 10)  # Right border
    
    # Totals Section
    totals_y = row_y - 60
    
    # Subtotal
    p.setFont("Helvetica", 11)
    p.drawString(420, totals_y, "Subtotal")
    p.drawString(500, totals_y, f"Rs {payment.paid_amount}")
    
    # Tax (if applicable)
    p.drawString(420, totals_y - 20, "Tax (0%)")
    p.drawString(520, totals_y - 20, "Rs 0.00")
    
    # Draw line above total
    p.setLineWidth(0.6)
    p.line(410, totals_y - 35, width - 55, totals_y - 35)
    
    # Total
    p.setFont("Helvetica-Bold", 14)
    p.drawString(420, totals_y - 50, "Total")
    p.drawString(500, totals_y - 50, f"Rs {payment.paid_amount}")
    
    # Thank you message
    p.setFont("Helvetica", 16)
    p.setFillColor(colors.black)
    p.drawString(50, totals_y - 120, "Thank you!")
    
    # Payment Information Section
    payment_info_y = totals_y - 180
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.black)
    p.drawString(50, payment_info_y, "PAYMENT INFORMATION")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, payment_info_y - 20, "Bank: Sampath Bank")
    p.drawString(50, payment_info_y - 35, f"Account Name: Sri Ganalaankra Maha Pirivena")
    p.drawString(50, payment_info_y - 50, "Account No.: 1064 5470 0910")
    
    # Payment due date
    due_date = datetime.now().strftime("%d %B %Y")
    p.drawString(50, payment_info_y - 65, f"Pay by: {due_date}")
    
    # Organization name at bottom right
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(dark_color)
    p.drawString(width - 250, payment_info_y - 20, "Sri Ganalaankra Maha Pirivena")
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawString(width - 250, payment_info_y - 35, "Peradeniya, Sri Lanka")
    
    # Additional payment details if needed
    if payment.balance > 0:
        p.setFont("Helvetica", 9)
        p.setFillColor(colors.red)
        p.drawString(50, payment_info_y - 90, f"Outstanding Balance: Rs {payment.balance}")
    
    # Footer
    p.setFont("Helvetica", 8)
    p.setFillColor(colors.gray)
    p.drawString(50, 50, "For any queries, please contact us at: nenalakara1985@gmail.com")
    p.drawString(50, 35, f"Generated on: {datetime.now().strftime('%d %B %Y at %H:%M')}")
    
    # Status watermark (if needed)
    if payment.status.upper() == 'PAID':
        p.setFont("Helvetica-Bold", 40)
        p.setFillColor(colors.Color(0, 0.8, 0, alpha=0.3))
        p.saveState()
        p.translate(width/2, height/2)
        p.rotate(45)
        text_width = p.stringWidth("PAID", "Helvetica-Bold", 40)
        p.drawString(-text_width/2, -20, "PAID")
        p.restoreState()
    elif payment.status.upper() == 'PENDING':
        p.setFont("Helvetica-Bold", 40)
        p.setFillColor(colors.Color(1, 0, 0, alpha=0.3))
        p.saveState()
        p.translate(width/2, height/2)
        p.rotate(45)
        text_width = p.stringWidth("PENDING", "Helvetica-Bold", 40)
        p.drawString(-text_width/2, -20, "PENDING")
        p.restoreState()
    elif payment.status.upper() == 'PARTIALLY':
        p.setFont("Helvetica-Bold", 40)
        p.setFillColor(colors.Color(0.8, 0.8, 0, alpha=0.3))
        p.saveState()
        p.translate(width/2, height/2)
        p.rotate(45)
        text_width = p.stringWidth("PARTIALLY", "Helvetica-Bold", 40)
        p.drawString(-text_width/2, -20, "PARTIALLY")
        p.restoreState()
    
    # Finalize the PDF
    p.showPage()
    p.save()
    
    # Get the PDF content
    pdf = buffer.getvalue()
    buffer.close()
    
    # Return the PDF as a downloadable response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.pk}_{payment.student.full_name.replace(" ", "_")}.pdf"'
    return response

# Alternative function if you want to display PDF in browser instead of download
def view_invoice_pdf(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    
    buffer = BytesIO()
    # ... (same code as above)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{payment.pk}.pdf"'
    return response