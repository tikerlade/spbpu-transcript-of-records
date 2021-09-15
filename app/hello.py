import json

import pandas as pd
import requests
import streamlit as st
from create_table_fpdf2 import PDF
from styleframe import StyleFrame, Styler

to_readable_columns_mapping = {
    "semester": "Семестр",
    "date": "Дата",
    "year": "Год",
    "hours": "Часы",
    "control_type": "Вид контроля",
    "mark": "Значение оценки",
    "mark_title": "Оценка",
    "scale": "Шкала",
    "subject": "Предмет",
    "subject_type": "Тип предмета",
    "zet": "Зач. единицы",
    "lecturers": "Преподаватель",
}
from_readable_columns_mapping = {v: k for k, v in to_readable_columns_mapping.items()}
printable_columns = [
    "subject",
    "control_type",
    "semester",
    "hours",
    "zet",
    "date",
    "lecturers",
    "mark_title",
]


def to_readable_columns(columns):
    new_columns = []

    for column in columns:
        new_columns.append(to_readable_columns_mapping[column])

    return new_columns


def from_readable_columns(columns):
    new_columns = []

    for column in columns:
        new_columns.append(from_readable_columns_mapping[column])

    return new_columns


def create_pdf(df):
    useful_columns = ["subject", "control_type", "semester", "date", "mark_title"]

    pdf = PDF()
    pdf.add_page()
    pdf.add_font("FreeSans", "", "FreeSans.ttf", uni=True)
    pdf.set_font("FreeSans", size=9)

    semesters = sorted(list(map(int, df.semester.unique())))
    for semester in semesters:
        data = df[df.semester == semester].applymap(str)
        year = data.year.iloc[0]
        data = data[useful_columns]
        semester_type = "Fall" if semester % 2 == 1 else "Spring"

        # print(data[useful_columns].to_dict(orient='list'))

        pdf.create_table(
            data.to_dict(orient="list"),
            title=f"Semester #{semester} ({semester_type} {year})",
        )
        pdf.ln()
    pdf.output("Grades.pdf")


def get_lk_data(identifier):
    cookies = {"PHPSESSID": identifier}
    response = requests.get(
        "https://lk.spbstu.ru/bitrix/vuz/api/marks2/", cookies=cookies
    )
    return json.loads(response.content)


def preprocess_lk_data(data):
    data = [subject["data"] for year in data for subject in year["semesters"]]
    data = [item for sublist in data for item in sublist]
    return data


st.set_page_config(page_title="My Dashboard", layout="wide", page_icon="📊")

# Greeting information
st.title("SPbPU Grades")
st.text(
    "HOWTO Get your identifier:\n\n"
    "1. Go to lk.spbstu.ru and login\n"
    "2. Open deveopers panel with F12 key\n"
    "3. Go to Application page\n"
    "4. Find Cookies named PHPSESSID\n"
    "5. DONE. This is your identifier for about next 30 minutes!\n\n"
)

identifier = st.text_input("Your identifier from lk.spbstu.ru:")

selected_columns = st.multiselect(
    "Select fields which you want to see in table:",
    to_readable_columns(printable_columns),
    to_readable_columns(printable_columns),
)
selected_columns = from_readable_columns(selected_columns)

if identifier:
    try:
        # Get and parse user data
        user_data = get_lk_data(identifier)
        df = pd.DataFrame(preprocess_lk_data(user_data))

        print(df.columns)
        # Compute GPA data
        gpa = df[df.mark > 1].mark.mean()

        semesters_gpa = df[df.mark > 1].groupby("semester").mark.mean()
        semesters_subjects = df.groupby("semester").mark.count()

        semesters_passed = df.semester.nunique()
        subjects = df.shape[0]

        # Save data as xlsx
        to_excel_df = df[selected_columns]
        to_excel_df.columns = to_readable_columns(to_excel_df.columns.values)

        sf = StyleFrame(to_excel_df)
        excel_writer = StyleFrame.ExcelWriter("Grades.xlsx")

        sf.apply_column_style(
            cols_to_style=to_excel_df.columns,
            styler_obj=Styler(horizontal_alignment="left", border_type="thin"),
            style_header=True,
        )
        sf.apply_headers_style(styler_obj=Styler(bold=True, border_type="thick"))

        sf.to_excel(excel_writer=excel_writer, best_fit=list(to_excel_df.columns))
        excel_writer.save()

        # Statistics as numbers
        st.markdown("## Numbers")
        first_kpi, second_kpi, third_kpi = st.columns(3)

        with first_kpi:
            st.markdown("**GPA**")
            st.markdown(
                f"<h1 style='text-align: center; color: red;'>{gpa}/5.0</h1>",
                unsafe_allow_html=True,
            )

        with second_kpi:
            st.markdown("**Semesters passed**")
            st.markdown(
                f"<h1 style='text-align: center; color: red;'>{semesters_passed}</h1>",
                unsafe_allow_html=True,
            )

        with third_kpi:
            st.markdown("**Subjects done**")
            st.markdown(
                f"<h1 style='text-align: center; color: red;'>{subjects}</h1>",
                unsafe_allow_html=True,
            )
        st.markdown("<hr/>", unsafe_allow_html=True)

        # Statistics as chart
        st.markdown("## Charts")
        first_chart, second_chart = st.columns(2)

        with second_chart:
            st.markdown("**GPA/semester**")
            st.bar_chart(semesters_gpa)

        with first_chart:
            st.markdown("**Subjects/semester**")
            st.bar_chart(semesters_subjects)

        with open("Grades.xlsx", "rb") as fout:
            download = st.download_button(
                "Download grades data as Excel 🗂",
                data=fout.read(),
                file_name="Grades.xlsx",
                mime="application/vnd.ms-excel",
            )

    except json.JSONDecodeError:
        st.text("Maybe this code is overdue. Try new one ...")
