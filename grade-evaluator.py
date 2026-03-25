#!/usr/bin/env python3
import csv
import os

FILE_NAME = "grades.csv"

def read_grades():
    if not os.path.exists(FILE_NAME):
        print("Error: grades.csv file not found.")
        return []

    data = []
    with open(FILE_NAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row:
                data.append(row)

    if len(data) == 0:
        print("Error: grades.csv is empty.")
        return []

    return data


def validate_data(data):
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    for row in data:
        score = float(row["score"])
        weight = float(row["weight"])
        category = row["assignment group"]

        if score < 0 or score > 100:
            print("Invalid score found.")
            return False

        total_weight += weight

        if category.lower() == "formative":
            formative_weight += weight
        else:
            summative_weight += weight

    if total_weight != 100:
        print("Total weight must be 100.")
        return False

    if formative_weight != 60:
        print("Formative weight must be 60.")
        return False

    if summative_weight != 40:
        print("Summative weight must be 40.")
        return False

    return True


def calculate(data):
    formative_total = 0
    summative_total = 0
    formative_weight = 0
    summative_weight = 0

    failed_formative = []

    for row in data:
        score = float(row["score"])
        weight = float(row["weight"])
        category = row["assignment group"]

        if category.lower() == "formative":
            formative_total += score * weight
            formative_weight += weight
            if score < 50:
                failed_formative.append(row)
        else:
            summative_total += score * weight
            summative_weight += weight

    formative_avg = formative_total / formative_weight
    summative_avg = summative_total / summative_weight
    total = (formative_total + summative_total) / 100
    gpa = (total / 100) * 5.0

    return formative_avg, summative_avg, total, gpa, failed_formative


def resubmissions(failed):
    if not failed:
        return []

    max_weight = max(float(row["weight"]) for row in failed)

    return [row["assignment"] for row in failed if float(row["weight"]) == max_weight]


def main():
    data = read_grades()
    if not data:
        return

    if not validate_data(data):
        return

    f_avg, s_avg, total, gpa, failed = calculate(data)

    print(f"Formative Score: {f_avg:.2f}%")
    print(f"Summative Score: {s_avg:.2f}%")
    print(f"Final Grade: {total:.2f}%")
    print(f"GPA: {gpa:.2f}")

    if f_avg >= 50 and s_avg >= 50:
        print("\nSTATUS: PASSED")
    else:
        print("\nSTATUS: FAILED")

    resub = resubmissions(failed)

    if resub:
        print("\nResubmission Required for:")
        for item in resub:
            print("-", item)


if __name__ == "__main__":
    main()
