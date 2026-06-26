import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

INPUT_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference_final_candidate.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference_final.csv"
AUDIT_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference_final_audit.csv"

FINAL_FIELDS = [
    "question_id",
    "question",
    "category",
    "reference_answer",
    "evidence_doc",
    "evidence_page",
    "evidence_text",
    "answerable",
    "notes",
]

UPDATES = {
    "Q001": {
        "question": "What office hours are stated for Federal Budgeting Process in Spring 2023?",
        "reference_answer": "Office hours are by appointment.",
    },
    "Q002": {
        "question": "What penalty is stated for more than two unexcused absences in 1. Syllabus 2023?",
        "reference_answer": "More than two unexcused absences will result in a drop of at least one letter grade.",
    },
    "Q003": {
        "question": "When are absences excused in 1. Syllabus 2023?",
        "reference_answer": "Absences are excused if they are supported by an appropriate document, such as documentation from the dean or a doctor.",
    },
    "Q004": {
        "question": "What penalty is stated for late assignments in 1. Syllabus 2023?",
        "reference_answer": "Assignments must be turned in on the due date; otherwise, students are subject to a drop of at least one letter grade per day.",
    },
    "Q005": {
        "question": "What grade consequence is stated for academic dishonesty in 1. Syllabus 2023?",
        "reference_answer": "Academic dishonesty in any form will not be tolerated and will result in a grade of zero.",
    },
    "Q006": {
        "question": "What is the final presentation requirement in 1. Syllabus 2023?",
        "reference_answer": "Each student will make a final presentation on an agency's FY 2024 budget proposal.",
    },
    "Q007": {
        "question": "How is the assessment divided in 1. Syllabus 2023?",
        "reference_answer": "The assessment consists of one-page memos worth 30%, the final presentation worth 30%, and overall class participation worth 40%.",
    },
    "Q008": {
        "question": "What assignment is due on February 11 in 1. Syllabus 2023?",
        "reference_answer": "The February 11 assignment is a one-page memo comparing an agency's FY 2021 budget for a specific program with the program's FY 2022 budget.",
    },
    "Q009": {
        "question": "What assignment is due on February 18 in 1. Syllabus 2023?",
        "reference_answer": "The February 18 assignment is a one-page memo comparing the President's FY 2023 budget request for a specific program within an agency to the program's FY 2022 budget.",
    },
    "Q010": {
        "question": "What topic is scheduled for February 21 in 1. Syllabus 2023?",
        "reference_answer": "The February 21 topic covers budget preparation, the President's budget, budget execution, and the agency budget formulation process.",
    },
    "Q011": {
        "question": "What budget is examined in 1. Syllabus 2023?",
        "reference_answer": "The syllabus states that students examine the President's FY 2023 budget.",
    },
    "Q012": {
        "question": "What office hours information is stated in 101-f22-syll?",
        "reference_answer": "The instructor's office hours are Wednesday 12:00-1:00 and by email. Teaching assistants also list office hours, including Friday 8:00-10:00, Monday/Wednesday 2:30-3:30, and Thursday 2:00-4:00.",
    },
    "Q013": {
        "question": "What topic related to dialect prejudice is stated in 101-f22-syll?",
        "reference_answer": "The course states that it will closely examine the pernicious effects of dialect prejudice.",
    },
    "Q014": {
        "question": "What file format is required for assignments in 101-f22-syll?",
        "reference_answer": "All assignments must be submitted in PDF format unless otherwise indicated.",
    },
    "Q015": {
        "question": "When and where are lectures held in 101-f22-syll?",
        "reference_answer": "Lectures are held on Monday and Wednesday from 1:25 to 2:15 in Morrill Science II, Room 131.",
    },
    "Q016": {
        "question": "Why should students attend discussion sections in 101-f22-syll?",
        "reference_answer": "Students should attend discussion sections because they will do group problem solving and mini-assignments there, which constitute a sizeable part of the grade.",
    },
    "Q017": {
        "question": "What should a student do if they are absent from discussion in 101-f22-syll?",
        "reference_answer": "The student should let the TA know; the syllabus states that the student will not be penalized and the TA will make an accommodation.",
    },
    "Q018": {
        "question": "How much of the course grade is made up by homework assignments in 101-f22-syll?",
        "reference_answer": "Homework assignments make up 50% of the course grade.",
    },
    "Q019": {
        "question": "How must assignments be submitted in 101-f22-syll?",
        "reference_answer": "Assignments must be typed and submitted electronically via Moodle in PDF format unless otherwise indicated.",
    },
    "Q020": {
        "question": "Where will assignment due dates be provided in 101-f22-syll?",
        "reference_answer": "Due dates will be given in the instructions for assignments.",
    },

    "Q021": {
        "question": "Which budget-related resources are listed in 1. Syllabus 2023?",
        "reference_answer": "The syllabus lists resources such as the Office of Management and Budget, the Congressional Budget Office, Congressional legislation information, past President budget proposals, and budget-related government resources.",
    },
    "Q022": {
        "question": "What rule applies to academic dishonesty in 1. Syllabus 2023?",
        "reference_answer": "Academic dishonesty in any form will not be tolerated and will result in a grade of zero.",
    },
    "Q023": {
        "question": "What class participation rule is stated in 1. Syllabus 2023?",
        "reference_answer": "Students must be prepared to actively participate during class.",
    },
    "Q024": {
        "question": "What assignment format rule is stated in 101-f22-syll?",
        "reference_answer": "All assignments must be submitted in PDF format unless otherwise indicated.",
    },
    "Q025": {
        "question": "Where will required class materials be posted in 101-f22-syll?",
        "reference_answer": "All class materials, including required readings, will be posted on Moodle.",
    },
    "Q026": {
        "question": "What does 101-f22-syll say about critical thought?",
        "reference_answer": "Critical thought is required in all areas of the course.",
    },
    "Q027": {
        "question": "What electronic submission rule is stated in 101-f22-syll?",
        "reference_answer": "Assignments must be typed and submitted electronically via Moodle in PDF format unless otherwise indicated.",
    },
    "Q028": {
        "question": "What academic dishonesty policy is stated in 101-f22-syll?",
        "reference_answer": "Students should become familiar with the university policy on academic dishonesty, including plagiarism, copying someone else's responses, and allowing others to copy their work.",
    },
    "Q029": {
        "question": "How does 101-f22-syll briefly define plagiarism?",
        "reference_answer": "Plagiarism refers to passing off someone else's work as your own.",
    },
    "Q030": {
        "question": "What forms of copying are considered academic dishonesty in 101-f22-syll?",
        "reference_answer": "Copying someone else's responses to assignments, projects, or exams, and allowing others to copy your work, are considered academic dishonesty.",
    },
    "Q031": {
        "question": "Is the book required in 130 syllabus 2 S 2023?",
        "reference_answer": "No. The book is recommended but not required, and it is available as an eText.",
    },
    "Q032": {
        "question": "What designation requirement is stated for Nutrition 130 in 130 syllabus 2 S 2023?",
        "reference_answer": "Nutrition 130 must meet certain criteria to meet the BS designation.",
    },
    "Q033": {
        "question": "What grading components are listed for Nutrition 130 in 130 syllabus 2 S 2023?",
        "reference_answer": "The listed grading components include four exams worth 36%, lecture iClicker questions worth 12%, in-class writing worth 8%, discussion attendance and participation worth 10%, and several homework or activity assignments.",
    },
    "Q034": {
        "category": "exception_handling",
        "question": "What exception affects make-up exam penalties in 130 syllabus 2 S 2023?",
        "reference_answer": "Students requesting a make-up exam after the actual exam are subject to a 20% grade penalty unless they can provide an excuse for missing the exam.",
    },
    "Q035": {
        "question": "When must the video or reading questionnaire questions be completed in 130 syllabus 2 S 2023?",
        "reference_answer": "They must be completed on the day the topic is presented in lecture.",
    },
    "Q036": {
        "question": "Will the analysis required for the questionnaire questions be on the exam in 130 syllabus 2 S 2023?",
        "reference_answer": "No. The analysis required to answer those questions will not be on the exam.",
    },
    "Q037": {
        "question": "What late submission penalty is stated in 130 syllabus 2 S 2023?",
        "reference_answer": "Late submissions are allowed, but there is a 10% deduction for every day the work is late.",
    },
    "Q038": {
        "question": "What must a student do if they are sick before discussion in 130 syllabus 2 S 2023?",
        "reference_answer": "The student must email their TA before the discussion if they are sick and have no medical note.",
    },
    "Q039": {
        "question": "What is required to earn full credit on video or reading questionnaires in 130 syllabus 2 S 2023?",
        "reference_answer": "To earn full credit, the writer must provide a thoughtful response.",
        "evidence_text": "To earn full credit on the Video/Reading Questionnaires the writer must provide a thoughtful response.",
    },
    "Q040": {
        "question": "What kind of answer is required for full credit on video or reading questionnaires in 130 syllabus 2 S 2023?",
        "reference_answer": "The answer must be thoughtful and accurate, answer the question posed, or defend an opinion accurately using information from the reading.",
    },

    "Q041": {
        "question": "If a student participates in discussion but has more than two unexcused absences in 1. Syllabus 2023, what should they understand?",
        "reference_answer": "Discussion participation is important, but more than two unexcused absences still result in a drop of at least one letter grade.",
    },
    "Q042": {
        "question": "If a student uses a cell phone in class and also has more than two unexcused absences in 1. Syllabus 2023, what policies apply?",
        "reference_answer": "Cell phone use is not permitted in the classroom, and more than two unexcused absences result in a drop of at least one letter grade.",
    },
    "Q043": {
        "question": "If a student does not participate and also has more than two unexcused absences in 1. Syllabus 2023, what should they understand?",
        "reference_answer": "Participation is necessary for building the class community, and more than two unexcused absences result in a drop of at least one letter grade.",
    },
    "Q044": {
        "question": "If a student participates inconsistently and has more than two unexcused absences in 1. Syllabus 2023, what grading issue may arise?",
        "reference_answer": "Consistent participation supports the class learning community, and more than two unexcused absences result in a drop of at least one letter grade.",
    },
    "Q045": {
        "question": "If a student has more than two absences but provides appropriate documentation in 1. Syllabus 2023, what should be considered?",
        "reference_answer": "More than two unexcused absences result in a grade drop, but absences may be excused if supported by appropriate documentation from the dean or a doctor.",
    },
    "Q046": {
        "question": "If a student has a documented absence and submits an assignment late in 1. Syllabus 2023, what policies are relevant?",
        "reference_answer": "A documented absence may be excused, but assignments must still be turned in on the due date or students may face a drop of at least one letter grade per day.",
    },
    "Q047": {
        "question": "If a student argues for fairness but turns in an assignment late in 1. Syllabus 2023, what rule still applies?",
        "reference_answer": "Fairness is emphasized, but assignments must be turned in on time or students may be subject to a drop of at least one letter grade per day.",
    },
    "Q048": {
        "question": "If all students are held to the same standards and an assignment is late in 1. Syllabus 2023, what consequence is stated?",
        "reference_answer": "All students are held to the same standards, and late assignments may result in a drop of at least one letter grade per day.",
    },
    "Q049": {
        "question": "If a student submits work late and also arrives late or leaves early in 1. Syllabus 2023, what two issues are stated?",
        "reference_answer": "Late assignments may result in a drop of at least one letter grade per day, and arriving late or leaving early disrupts the flow of the class.",
    },
    "Q050": {
        "question": "If a student disrupts class by arriving late and also commits academic dishonesty in 1. Syllabus 2023, what policies apply?",
        "reference_answer": "Arriving late or leaving early disrupts the class, and academic dishonesty in any form results in a grade of zero.",
    },
    "Q051": {
        "question": "If a student needs to arrive late or leave early and also must avoid academic dishonesty in 1. Syllabus 2023, what should they understand?",
        "reference_answer": "Late arrivals or early departures should be exceptions and require prior consultation, while academic dishonesty is not tolerated and results in a grade of zero.",
    },
    "Q052": {
        "question": "If a student attends lectures but skips discussion sections in 101-f22-syll, what grading-related issue is stated?",
        "reference_answer": "Lectures meet on Monday and Wednesday, but discussion sections are on Friday and include group problem solving and mini-assignments that constitute a sizeable part of the grade.",
    },
    "Q053": {
        "question": "If a student cannot attend discussion in 101-f22-syll, what should they do and why?",
        "reference_answer": "Discussion sections contribute to the grade, but if a student is absent, they should let the TA know so the TA can make an accommodation.",
    },
    "Q054": {
        "question": "If a student misses one homework assignment in 101-f22-syll, why could that matter for the course grade?",
        "reference_answer": "Homework assignments make up 50% of the course grade, so missing one assignment could lower the grade considerably.",
    },
    "Q055": {
        "question": "If homework is a large part of the grade in 101-f22-syll, how must assignments be submitted?",
        "reference_answer": "Homework assignments make up 50% of the grade, and assignments must be typed and submitted electronically via Moodle in PDF format unless otherwise indicated.",
    },

    "Q056": {
        "category": "rule_understanding",
        "question": "What attendance penalty applies to more than two unexcused absences in 1. Syllabus 2023?",
        "reference_answer": "More than two unexcused absences result in a drop of at least one letter grade.",
    },
    "Q057": {
        "question": "Under what condition are absences excused in 1. Syllabus 2023?",
        "reference_answer": "Absences are excused if supported by an appropriate document, such as documentation from the dean or a doctor.",
    },
    "Q058": {
        "question": "What special-case rule applies to late arrivals or early departures in 1. Syllabus 2023?",
        "reference_answer": "Late arrivals or early departures should be exceptions and should occur only with prior consultation.",
    },
    "Q059": {
        "question": "What exception is stated to the PDF assignment submission requirement in 101-f22-syll?",
        "reference_answer": "Assignments must be submitted in PDF format unless otherwise indicated.",
    },
    "Q060": {
        "question": "What accommodation is stated for a student's absence in 101-f22-syll?",
        "reference_answer": "The student will not be penalized for the absence if they let the TA know, and the TA will make an accommodation.",
    },
    "Q061": {
        "question": "What disability accommodation statement is made in 101-f22-syll?",
        "reference_answer": "Many accommodations are available at the university to ensure that students with disabilities participate fully in academic and student life.",
    },
    "Q062": {
        "question": "What access goal is stated for students with disabilities in 101-f22-syll?",
        "reference_answer": "Accommodations provide students with disabilities equal access to the educational and co-curricular process without compromising essential curriculum components.",
    },
    "Q063": {
        "question": "How are accommodations determined in 101-f22-syll?",
        "reference_answer": "Accommodations are determined on an individual basis based on the student's documentation.",
    },
    "Q064": {
        "question": "Who may be eligible for accommodations in 101-f22-syll?",
        "reference_answer": "A student with a documented disability on file with Disability Services may be eligible for accommodations in the course.",
    },
    "Q065": {
        "question": "What should students with documented disabilities do if they require accommodations in 101-f22-syll?",
        "reference_answer": "They should let the instructor know as soon as possible.",
    },
    "Q066": {
        "question": "Who should students contact for course accommodation and disability information in 101-f22-syll?",
        "reference_answer": "Students should contact Disability Services for information about course accommodation and disability.",
        "evidence_text": "For information about course accommodation and disability, contact Disability Services.",
    },
    "Q067": {
        "question": "What office must have a documented disability on file for accommodation eligibility in 101-f22-syll?",
        "reference_answer": "The documented disability must be on file with Disability Services for the student to be eligible for accommodations.",
    },
    "Q068": {
        "question": "What exception is stated for typed electronic PDF submissions in 101-f22-syll?",
        "reference_answer": "Assignments must be typed and submitted electronically via Moodle in PDF format unless otherwise indicated.",
    },
    "Q069": {
        "question": "When may the stated PDF submission format not apply in 101-f22-syll?",
        "reference_answer": "The PDF submission requirement may not apply when otherwise indicated.",
        "evidence_text": "All assignments must be submitted in pdf format unless otherwise indicated.",
    },
    "Q070": {
        "question": "When will exceptions be made for religious observance or serious illness in 101-f22-syll?",
        "reference_answer": "Exceptions will be made when the student provides advance notice of religious observance or written documentation for serious illness or another compelling event.",
    },
}

UNANSWERABLE_IDS = {f"Q{i:03d}" for i in range(71, 81)}

def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def main():
    df = pd.read_csv(INPUT_FILE, dtype=str).fillna("")

    # Basic normalization
    for col in df.columns:
        df[col] = df[col].apply(clean_text)

    # Apply manual updates
    for qid, changes in UPDATES.items():
        mask = df["question_id"] == qid
        if not mask.any():
            print(f"WARNING: {qid} not found")
            continue

        for col, value in changes.items():
            df.loc[mask, col] = value

        # Mark as reviewed in audit file
        if "quality_flags" in df.columns:
            df.loc[mask, "quality_flags"] = ""

    # Fix unanswerable rows
    mask_unanswerable = df["question_id"].isin(UNANSWERABLE_IDS)

    df.loc[mask_unanswerable, "answerable"] = "no"
    df.loc[mask_unanswerable, "evidence_doc"] = "N/A"
    df.loc[mask_unanswerable, "evidence_page"] = "N/A"
    df.loc[mask_unanswerable, "evidence_text"] = "N/A"
    df.loc[
        mask_unanswerable,
        "reference_answer"
    ] = "The provided course documents do not contain enough information to answer this question."

    if "quality_flags" in df.columns:
        df.loc[mask_unanswerable, "quality_flags"] = ""

    # Ensure answerable rows are yes
    df.loc[~mask_unanswerable, "answerable"] = "yes"

    # Normalize evidence_page
    df["evidence_page"] = df["evidence_page"].replace({"1.0": "1"})

    # Save audit file with quality_flags if present
    df.to_csv(AUDIT_FILE, index=False, encoding="utf-8-sig")

    # Save final file without quality_flags
    final_df = df[FINAL_FIELDS].copy()
    final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Saved final file: {OUTPUT_FILE}")
    print(f"Saved audit file: {AUDIT_FILE}")
    print()
    print("Rows:", len(final_df))
    print()
    print("Category counts:")
    print(final_df["category"].value_counts())
    print()
    print("Answerable counts:")
    print(final_df["answerable"].value_counts())

    print()
    print("Duplicate question check:")
    dup = final_df[final_df["question"].duplicated(keep=False)]
    print("Duplicate questions:", len(dup))
    if len(dup) > 0:
        print(dup[["question_id", "question"]].to_string(index=False))

if __name__ == "__main__":
    main()
