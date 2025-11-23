import json
from io import BytesIO
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
from .utils import analyze_csv

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "CSV file not provided"}, status=400)

    csv_file = request.FILES['file']

    # Save file
    # file_path = default_storage.save(csv_file.name, csv_file)

    saved_name = default_storage.save(f"uploads/{csv_file.name}",csv_file)

    # Analyze
    result = analyze_csv(saved_name)

    # Save in DB
    dataset = EquipmentDataset.objects.create(
        file=saved_name,
        total_count=result["total_count"],
        
        avg_flowrate=result["avg_flowrate"],
        avg_pressure=result["avg_pressure"],
        avg_temperature=result["avg_temperature"],
        type_distribution=result["type_distribution"],

        min_flowrate=result["min_flowrate"],
        min_pressure=result["min_pressure"],
        min_temperature=result["min_temperature"],

        max_flowrate=result["max_flowrate"],
        max_pressure=result["max_pressure"],
        max_temperature=result["max_temperature"],

        rows = result['rows'],
        # Min-Max Info
        # min_flowrate = result
    )

    # Keep only last 5 entries
    qs = EquipmentDataset.objects.order_by('-uploaded_at')
    if qs.count() > 5:
        for old in qs[5:]:
            old.delete()

    serializer = EquipmentDatasetSerializer(dataset)
    return Response(serializer.data, status=201)



# @api_view(['POST'])
# def upload_csv(request):
#     # debug: show what was received
#     print("DEBUG: request.FILES keys:", list(request.FILES.keys()))

#     # accept common field names or fallback to first file
#     csv_file = request.FILES.get('file') or request.FILES.get('csv') or (next(iter(request.FILES.values()), None))
#     if csv_file is None:
#         return Response({"error": "CSV file not provided. Use form-data key 'file'."}, status=400)

#     saved_name = default_storage.save(f"uploads/{csv_file.name}", csv_file)
#     file_disk_path = default_storage.path(saved_name)
#     print("DEBUG: saved file to:", file_disk_path)

#     try:
#         result = analyze_csv(file_disk_path)
#     except ValueError as ve:
#         # validation/read errors become 400 with message
#         print("DEBUG: analyze_csv ValueError:", str(ve))
#         return Response({"error": str(ve)}, status=400)
#     except Exception as e:
#         import traceback; traceback.print_exc()
#         return Response({"error": "Unexpected server error while parsing CSV."}, status=500)

#     # debug: print analyzer output to confirm keys
#     print("DEBUG: analyze_csv returned:", result)

#     # defensive: ensure expected keys exist
#     required_keys = ("total_count", "avg_flowrate", "avg_pressure", "avg_temperature", "type_distribution")
#     if not all(k in result for k in required_keys):
#         print("DEBUG: Missing keys in result:", [k for k in required_keys if k not in result])
#         return Response({"error": "Analyzer returned unexpected result. Check server logs."}, status=500)

#     dataset = EquipmentDataset.objects.create(
#         file=saved_name,
#         total_count=result["total_count"],
#         avg_flowrate=result["avg_flowrate"],
#         avg_pressure=result["avg_pressure"],
#         avg_temperature=result["avg_temperature"],
#         type_distribution=result["type_distribution"]
#     )

#     # keep last 5
#     qs = EquipmentDataset.objects.order_by('-uploaded_at')
#     if qs.count() > 5:
#         for old in qs[5:]:
#             old.delete()

#     serializer = EquipmentDatasetSerializer(dataset)
#     return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)

# TO-DO add pdf download opton

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_report_pdf(request, pk):
    """
    Generate a simple PDF report for dataset `pk` and return as FileResponse.
    """
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
    except EquipmentDataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=404)

    # Create a bytes buffer for the PDF
    buffer = BytesIO()

    # Create a canvas (ReportLab)
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Margins
    left = 20 * mm
    top = height - 20 * mm
    line_h = 8 * mm

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(left, top, f"Dataset Report — ID {dataset.id}")

    p.setFont("Helvetica", 10)
    p.drawString(left, top - 1.2 * line_h, f"Uploaded: {dataset.uploaded_at.isoformat()}")

    # Summary box
    y = top - 2.6 * line_h
    p.setFont("Helvetica-Bold", 12)
    p.drawString(left, y, "Summary")
    y -= 1.1 * line_h
    p.setFont("Helvetica", 10)

    def draw_kv(key, value, indent=0):
        nonlocal y
        p.drawString(left + indent, y, f"{key}: {value}")
        y -= 0.9 * line_h

    draw_kv("Total count", getattr(dataset, "total_count", "N/A"))
    draw_kv("Avg Flowrate", getattr(dataset, "avg_flowrate", "N/A"))
    draw_kv("Avg Pressure", getattr(dataset, "avg_pressure", "N/A"))
    draw_kv("Avg Temperature", getattr(dataset, "avg_temperature", "N/A"))
    draw_kv("Min Flowrate", getattr(dataset, "min_flowrate", "N/A"))
    draw_kv("Max Flowrate", getattr(dataset, "max_flowrate", "N/A"))
    draw_kv("Min Pressure", getattr(dataset, "min_pressure", "N/A"))
    draw_kv("Max Pressure", getattr(dataset, "max_pressure", "N/A"))
    draw_kv("Min Temperature", getattr(dataset, "min_temperature", "N/A"))
    draw_kv("Max Temperature", getattr(dataset, "max_temperature", "N/A"))

    # Leave a bit of space before distribution
    y -= 0.5 * line_h

    # Type distribution
    p.setFont("Helvetica-Bold", 12)
    p.drawString(left, y, "Type Distribution")
    y -= 1.1 * line_h
    p.setFont("Helvetica", 10)

    # dataset.type_distribution assumed to be dict or JSONField
    td = dataset.type_distribution or {}
    # If stored as string, try parse
    if isinstance(td, str):
        try:
            td = json.loads(td)
        except Exception:
            td = {}

    # Draw as simple two-column table
    p.drawString(left, y, "Type")
    p.drawString(left + 80 * mm, y, "Count")
    y -= 0.9 * line_h

    for tp, cnt in td.items():
        # If out of space, add a new page
        if y < 40 * mm:
            p.showPage()
            y = top - 20 * mm
            p.setFont("Helvetica", 10)

        p.drawString(left, y, str(tp))
        p.drawString(left + 80 * mm, y, str(cnt))
        y -= 0.8 * line_h

    # Optionally include original CSV path (local path). We include it as text:
    y -= 1.1 * line_h
    p.setFont("Helvetica-Bold", 10)
    p.drawString(left, y, "Source file (local path):")
    y -= 0.9 * line_h
    p.setFont("Helvetica", 9)
    src = dataset.file.name if dataset.file else "N/A"
    # Draw multi-line if long
    text_obj = p.beginText(left, y)
    text_obj.setFont("Helvetica", 9)
    max_width = width - 2 * left
    # naive wrap: split at spaces
    for part in str(src).split():
        text_obj.textLine(part)
    p.drawText(text_obj)

    # Finalize
    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"dataset_{dataset.id}_report.pdf"

    return FileResponse(buffer, as_attachment=True, filename=filename)
