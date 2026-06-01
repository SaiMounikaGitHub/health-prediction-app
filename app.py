from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from datetime import datetime

from email_validator import (
    validate_email,
    EmailNotValidError
)

from config import Config

from models.patient_model import (
    db,
    Patient
)

from services.prediction_service import (
    generate_health_prediction
)


# Initialize Flask App

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


# Create Database Tables

with app.app_context():

    db.create_all()


# Home Page

@app.route("/")

def index():

    patients = Patient.query.all()

    return render_template(

        "index.html",

        patients=patients
    )


# Add Patient

@app.route(

    "/add",

    methods=["GET", "POST"]
)

def add_patient():

    if request.method == "POST":

        full_name = request.form[
            "full_name"
        ]

        dob = request.form[
            "dob"
        ]

        email = request.form[
            "email"
        ]

        glucose = request.form[
            "glucose"
        ]

        haemoglobin = request.form[
            "haemoglobin"
        ]

        cholesterol = request.form[
            "cholesterol"
        ]

        try:

            # Validate Email

            validate_email(email)

            # Validate DOB

            dob_date = datetime.strptime(

                dob,

                "%Y-%m-%d"
            )

            if dob_date > datetime.now():

                return (
                    "Date of birth "
                    "cannot be future date"
                )

            # Validate Numeric Values

            glucose = float(glucose)

            haemoglobin = float(
                haemoglobin
            )

            cholesterol = float(
                cholesterol
            )

        except EmailNotValidError:

            return "Invalid Email"

        except ValueError:

            return (
                "Blood values must "
                "be numeric"
            )

        # Generate AI Prediction

        remarks = generate_health_prediction(

            glucose,

            haemoglobin,

            cholesterol
        )

        # Create Patient Object

        patient = Patient(

            full_name=full_name,

            dob=dob,

            email=email,

            glucose=glucose,

            haemoglobin=haemoglobin,

            cholesterol=cholesterol,

            remarks=remarks
        )

        db.session.add(patient)

        db.session.commit()

        return redirect(

            url_for("index")
        )

    return render_template(
        "add_patient.html"
    )


# Edit Patient

@app.route(

    "/edit/<int:id>",

    methods=["GET", "POST"]
)

def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        try:

            patient.full_name = request.form[
                "full_name"
            ]

            patient.dob = request.form[
                "dob"
            ]

            patient.email = request.form[
                "email"
            ]

            # Validate Email

            validate_email(
                patient.email
            )

            # Validate DOB

            dob_date = datetime.strptime(

                patient.dob,

                "%Y-%m-%d"
            )

            if dob_date > datetime.now():

                return (
                    "Date of birth "
                    "cannot be future date"
                )

            # Convert Numeric Values

            patient.glucose = float(

                request.form[
                    "glucose"
                ]
            )

            patient.haemoglobin = float(

                request.form[
                    "haemoglobin"
                ]
            )

            patient.cholesterol = float(

                request.form[
                    "cholesterol"
                ]
            )

            # Regenerate AI Prediction

            patient.remarks = (

                generate_health_prediction(

                    patient.glucose,

                    patient.haemoglobin,

                    patient.cholesterol
                )
            )

            db.session.commit()

            return redirect(

                url_for("index")
            )

        except EmailNotValidError:

            return "Invalid Email"

        except ValueError:

            return (
                "Blood values must "
                "be numeric"
            )

    return render_template(

        "edit_patient.html",

        patient=patient
    )


# Delete Patient

@app.route("/delete/<int:id>")

def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)

    db.session.commit()

    return redirect(

        url_for("index")
    )


# Run Flask App

if __name__ == "__main__":

    app.run(debug=True)

