import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import chartGen as Cg
import os


def Generate_Report(database):
    if not os.path.isdir(".\\Reports"):
        os.mkdir(".\\Reports")

    path = "Reports\\"
    with open(database) as file:
        header = csv.reader(file)
        header = next(header)

    with open(database) as data:
        read = csv.DictReader(data)
        for i in read:

            name = i["name"]
            marks = [i[header[x]] for x in range(4, 9)]
            Cmarks = [int(mark) for mark in marks]
            chart = Cg.barChart()
            chart.generate(
                marks=Cmarks, subjects=[header[x] for x in range(4, 9)], name=name
            )

            file = canvas.Canvas(f"{path}{i['name']}.pdf", pagesize=A4)
            file.drawString(240, 800, "REPORT")
            file.drawString(200 - 108 - 20, 700 + 50, "Name :")
            file.drawString(242 - 108 - 20, 700 + 50, i["name"])
            file.drawString(200 - 108 - 20, 700 + 50 - 20, "Admission Number :")
            file.drawString(242 - 39 - 20, 700 + 50 - 20, i["admin"])
            file.drawString(200 - 108 - 20, 700 + 50 - 40, "Class :")
            file.drawString(242 - 112 - 20, 700 + 50 - 40, i["class"])
            file.drawString(200 - 108 - 20, 700 + 50 - 60, "Section :")
            file.drawString(242 - 101 - 20, 700 + 50 - 60, i["section"])

            file.drawString(200 - 108 - 20, 700 + 50 - 120, f"{header[4]}")
            file.drawString(200 - 10 - 20, 700 + 50 - 120, ": ")
            file.drawString(205 - 0 - 20, 700 + 50 - 120, i[header[4]])
            file.drawString(200 - 108 - 20, 700 + 50 - 140, f"{header[5]}")
            file.drawString(200 - 10 - 20, 700 + 50 - 140, ": ")
            file.drawString(205 - 0 - 20, 700 + 50 - 140, i[header[5]])
            file.drawString(200 - 108 - 20, 700 + 50 - 160, f"{header[6]}")
            file.drawString(200 - 10 - 20, 700 + 50 - 160, ": ")
            file.drawString(205 - 0 - 20, 700 + 50 - 160, i[header[6]])
            file.drawString(200 - 108 - 20, 700 + 50 - 180, f"{header[7]}")
            file.drawString(200 - 10 - 20, 700 + 50 - 180, ": ")
            file.drawString(205 - 0 - 20, 700 + 50 - 180, i[header[7]])
            file.drawString(200 - 108 - 20, 700 + 50 - 200, f"{header[8]}")
            file.drawString(200 - 10 - 20, 700 + 50 - 200, ": ")
            file.drawString(205 - 0 - 20, 700 + 50 - 200, i[header[8]])

            file.drawInlineImage(f"charts\\ppm\\{name}.ppm", 242, 500)

            file.save()


if __name__ == "__main__":
    dbPath = input("Enter your csv file path : ")
    try:
        Generate_Report(database=dbPath)
    except Exception as e:
        print(e.message)
        input("\nPress enter to continue...")
