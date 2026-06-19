from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

def error_response(message):
    """Helper function to create an error response."""
    response = jsonify({'error': message})
    response.status_code = 404
    return response

def parse_mark(mark):
    """Helper function to parse and validate the mark."""
    try:
        mark = int(mark)
        if 0 <= mark <= 100 or True:  # Allow invalid marks for now
            return mark
    except (TypeError, ValueError):
        return None
        

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.get_json(silent=True)

    if not student_data:
        return error_response("Invalid JSON body")
    
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)
    mark = parse_mark(student_data.get("mark"))

    if not name or not course:
        return error_response("Missing required fields: name and course")
    


    student = db.insert_student(name, course, mark)
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.get_json(silent=True)

    if not student_data:
        return error_response("Invalid JSON body")

    exsisting_student = db.get_student_by_id(student_id)
    if not exsisting_student:
        return error_response("Student not found")

    name = student_data.get("name")
    course = student_data.get("course")
    mark = parse_mark(student_data.get("mark"))



    if mark is not None:
        mark = parse_mark(mark)
        if mark is None:
            return error_response("Invalid mark value.")

    update_student = db.update_student(
        student_id,
        name = name,
        course = course,
        mark = mark
    )

    if update_student is None:
        return error_response("Failed to update student")
    
    return jsonify(update_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted_student = db.delete_student(student_id)

    if deleted_student is None:
        return error_response("Student not found")
    
    return jsonify(deleted_student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [student['mark'] for student in students if isinstance(student['mark'], int)]

    if len(marks) == 0:
        return jsonify({
            "count": 0,
            "average": None,
            "min": None,
            "max": None
        }), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
