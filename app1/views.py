from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import FileUploadForm
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from django.core.mail import EmailMessage


matplotlib.use('Agg')
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print(file)
            try:
                # Read the uploaded file into a DataFrame
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    return HttpResponse("Invalid file type", status=400)
                
                summary = df.groupby('Cust State')['DPD'].sum().reset_index()

                plt.figure(figsize=(10, 6))
                plt.bar(summary['Cust State'], summary['DPD'], color='orange')
                plt.xlabel('Cust State')
                plt.ylabel('Total DPD')
                plt.title('Total DPD by Cust State')
                plt.xticks(rotation=45, ha='right')
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                output_image_path = os.path.join(settings.STATIC_ROOT, 'dpd_summary_report.png')
                print(output_image_path)
                plt.savefig(output_image_path, bbox_inches='tight')
                plt.close() 

                email_subject = 'Python Assignment- Devanand J'
                email_body = 'Please find attached the DPD summary report.'
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['tech@themedius.ai', 'yash@themedius.ai'],
                )

                # Attach the image to the email
                email.attach_file(output_image_path)
                email.send()
                
                image_url = settings.MEDIA_URL + 'dpd_summary_report.png'
                return render(request, 'upload.html', {'form': form, 'image_url': image_url})

            except Exception as e:
                return HttpResponse(f"Error processing file: {e}", status=400)
    else:
        form = FileUploadForm()
    
    return render(request, 'upload.html', {'form': form})
