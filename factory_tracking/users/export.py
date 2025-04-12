import csv
from io import StringIO, BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def export_pdf(machines):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Machine Status Report")
    p.setFont("Helvetica", 10)
    y -= 30

    for machine in machines:
        collections = ", ".join([c.name for c in machine.collections.all()])
        p.drawString(50, y, f"{machine.name} ({machine.status}) — Collections: {collections}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="machines.pdf"'
    return response


def export_csv(machines):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["ID", "Name", "Status", "Collections"])

    for machine in machines:
        collections = ", ".join([c.name for c in machine.collections.all()])
        writer.writerow([machine.id, machine.name, machine.status, collections])

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="machines.csv"'
    return response
