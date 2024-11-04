from marshmallow import Schema, fields, validate

# Patient Schema
class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=0))
    gender = fields.Str(required=True, validate=validate.OneOf(["Male", "Female", "Other"]))
    medical_history = fields.Str()

class PatientSchema(PlainPatientSchema):
    appointments = fields.List(fields.Nested("AppointmentSchema", dump_only=True))
    room_id = fields.Int(load_only=True)

# Doctor Schema
class PlainDoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    specialization = fields.Str(required=True)
    availability = fields.Str()

class DoctorSchema(PlainDoctorSchema):
    appointments = fields.List(fields.Nested("AppointmentSchema", dump_only=True))
    department_id = fields.Int(load_only=True)

# Room Schema
class PlainRoomSchema(Schema):
    id = fields.Int(dump_only=True)
    ward_id = fields.Int(load_only=True)
    patient_id = fields.Int(load_only=True)
    bed_number = fields.Str(required=True)
    room_status = fields.Str(required=True)

class RoomSchema(PlainRoomSchema):
    ward = fields.Nested("WardSchema", dump_only=True)
    patient = fields.Nested("PatientSchema", dump_only=True)

# Ward Schema
class PlainWardSchema(Schema):
    id = fields.Int(dump_only=True)
    ward_name = fields.Str(required=True)
    capacity = fields.Int(required=True)
    current_occupancy = fields.Int()

class WardSchema(PlainWardSchema):
    rooms = fields.List(fields.Nested("RoomSchema", dump_only=True))

# Appointment Schema
class PlainAppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(load_only=True)
    doctor_id = fields.Int(load_only=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)

class AppointmentSchema(PlainAppointmentSchema):
    patient = fields.Nested("PatientSchema", dump_only=True)
    doctor = fields.Nested("DoctorSchema", dump_only=True)
    prescription = fields.Nested("PrescriptionSchema", dump_only=True)

# Prescription Schema
class PlainPrescriptionSchema(Schema):
    id = fields.Int(dump_only=True)
    appointment_id = fields.Int(load_only=True)
    medicine_details = fields.Str(required=True)
    dosage_details = fields.Str(required=True)
    duration_days = fields.Int(required=True)

class PrescriptionSchema(PlainPrescriptionSchema):
    appointment = fields.Nested("AppointmentSchema", dump_only=True)

# Billing Schema
class PlainBillingSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(load_only=True)
    doctor_id = fields.Int(load_only=True)
    total_amount = fields.Float(required=True)
    date = fields.Date(required=True)
    payment_status = fields.Str(required=True)

class BillingSchema(PlainBillingSchema):
    patient = fields.Nested("PatientSchema", dump_only=True)
    doctor = fields.Nested("DoctorSchema", dump_only=True)

# Department Schema
class PlainDepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    department_name = fields.Str(required=True)
    head_of_department = fields.Str(required=True)

class DepartmentSchema(PlainDepartmentSchema):
    doctors = fields.List(fields.Nested("DoctorSchema", dump_only=True))
    employees = fields.List(fields.Nested("EmployeeSchema", dump_only=True))

# Employee Schema
class PlainEmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    role = fields.Str(required=True)
    salary = fields.Float(required=True)
    hire_date = fields.Date(required=True)
    department_id = fields.Int(load_only=True)

class EmployeeSchema(PlainEmployeeSchema):
    department = fields.Nested("DepartmentSchema", dump_only=True)
