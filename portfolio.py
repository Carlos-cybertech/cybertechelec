from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from sqlalchemy import extract
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from auth import login_required
import models
from models import get_db
from utils import objects_to_dict
from utils import extract_form_data, validate_form_data, clean_form_data

bp = Blueprint("portfolio", __name__)


@bp.route("/")
@login_required
def index():
    return render_template("portfolio/index.html")


@bp.route("/portfolio/search")
@login_required
def search():

    q = request.args.get("q")
    db = get_db()
    if q:
        projects = db.query(models.Project).join(models.User).filter(models.User.id == session["user_id"], models.Project.address.like(f"%{q}%")).all()
        projects = [objects_to_dict(project) for project in projects]
    else:
        projects = []
    return jsonify(projects)


@bp.route("/portfolio/newproject", methods=["GET", "POST"])
@login_required
def newproject():

    if request.method == "POST":

        form_data = extract_form_data()
        error = validate_form_data(form_data)
        
        if error:
            flash(error, "danger")

            project_status = ["completed", "in_progress", "pending", "on_hold"]
            i_type = ["underground", "rough", "power_release", "final", "pending"]
            inspection_status = ["passed", "rescheduled", "pending"]
            p_type = ["dwp", "sce"]
            invoice = ["50%", "90%", "100%"]
            datto = ["completed", "in_progress", "pending"]

            return render_template("portfolio/newproject.html", project_status=project_status, i_type=i_type, inspection_status=inspection_status, p_type=p_type, invoice=invoice, datto=datto, form_data=form_data)
        
        form_data = clean_form_data(form_data)

        db = get_db()
        new_project = models.Project(
            p_type=form_data["p_type"],
            po_number=form_data["po_number"],
            address=form_data["address"],
            num_chargers=form_data["num_chargers"],
            permit_num1=form_data["permit_num1"],
            permit_num2=form_data["permit_num2"],
            project_status=form_data["project_status"],
            start_date=form_data["start_date"],
            invoice=form_data["invoice"],
            datto=form_data["datto"],
            notes=form_data["notes"],
            user_id=session["user_id"]
        )
        
        try:
            db.add(new_project)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            print(f"Full error message: {str(e)}")  # Log the full error message
            #print(f"Error message: {str(e.orig)}")  # Log the error message
            if "UNIQUE constraint failed" in str(e.orig):
                if "po_number" in str(e.orig):
                    error = f"Error: The po_number {form_data['po_number']} is already taken. Please verify your inserting data."
                elif "address" in str(e.orig):
                    error = f"Error: The address {form_data['address']} is already taken. Please verify your inserting data."
                else:
                    error = "Error: A unique constraint was violated."
            else:
                error = "An integrity error occurred."
        else:
            project_id = new_project.id

            new_inspection = models.Inspection(
                i_type1=form_data["i_type1"],
                inspection_status1=form_data["inspection_status1"],
                inspection_date1=form_data["inspection_date1"],
                i_type2=form_data["i_type2"],
                inspection_status2=form_data["inspection_status2"],
                inspection_date2=form_data["inspection_date2"],
                i_type3=form_data["i_type3"],
                inspection_status3=form_data["inspection_status3"],
                inspection_date3=form_data["inspection_date3"],
                project_id=project_id
                )
            db.add(new_inspection)
            db.commit()
            inspection_id=new_inspection.id
    
            new_compositekey = models.CompositeKey(
                user_id=session["user_id"],
                project_id=project_id,
                inspection_id=inspection_id
            )
            db.add(new_compositekey)
            db.commit()
    
            flash("Project Saved!", "primary")
            return redirect(url_for("portfolio.summary"))
            
        if error:
            flash(error, "danger")

            project_status = ["completed", "in_progress", "pending", "on_hold"]
            i_type = ["underground", "rough", "power_release", "final", "pending"]
            inspection_status = ["passed", "rescheduled", "pending"]
            p_type = ["dwp", "sce"]
            invoice = ["50%", "90%", "100%"]
            datto = ["completed", "in_progress", "pending"]

            return render_template("portfolio/newproject.html", project_status=project_status, i_type=i_type, inspection_status=inspection_status, p_type=p_type, invoice=invoice, datto=datto, form_data=form_data)
            

    else:
        project_status = ["completed", "in_progress", "pending", "on_hold"]
        i_type = ["underground", "rough", "power_release", "final", "pending"]
        inspection_status = ["passed", "rescheduled", "pending"]
        p_type = ["dwp", "sce"]
        invoice = ["50%", "90%", "100%"]
        datto = ["completed", "in_progress", "pending"]

        form_data = extract_form_data()

        return render_template("portfolio/newproject.html", project_status=project_status, i_type=i_type, inspection_status=inspection_status, p_type=p_type, invoice=invoice, datto=datto, form_data=form_data)


@bp.route("/portfolio/utils", methods=["POST"])
@login_required
def utils():
    """Filter projects, by type."""
    db = get_db()

    p_type = request.form.get("dropdown")

    if p_type == "dwp":
        projects = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"], models.Project.p_type == p_type).order_by(models.Project.start_date.desc()).all()

        return render_template("portfolio/utils.html", projects=projects, p_type=p_type)

    elif p_type == "sce":
        projects = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"], models.Project.p_type == p_type).order_by(models.Project.start_date.desc()).all()

        return render_template("portfolio/utils.html", projects=projects, p_type=p_type)
    

@bp.route("/portfolio/summary", methods=['GET'])
@login_required
def summary():
    """Summary"""

    current_year = datetime.now().year

    db = get_db()
    
    projects = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"], extract('year', models.Project.start_date) == current_year).order_by(models.Project.start_date.desc()).all()

    years = db.query(extract('year', models.Project.start_date).distinct().label('year')).order_by('year').all()
    years = [year.year for year in years]

    return render_template("portfolio/summary.html", projects=projects, years=years)


@bp.route("/portfolio/project_status", methods=['GET'])
@login_required
def project_status():
    """Filter projects, by project status and by start_date year"""
    db = get_db()

    years = db.query(extract('year', models.Project.start_date).distinct().label('year')).order_by('year').all()
    years = [year.year for year in years]

    project_status_filter = request.args.get("project_status")
   
    query = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"])

    if project_status_filter:
        query = query.filter(models.Project.project_status == project_status_filter)

    projects = query.order_by(models.Project.start_date.desc()).all()

    return render_template("portfolio/project_status.html", projects=projects, years=years, project_status_filter=project_status_filter)


@bp.route("/portfolio/project_year", methods=['GET'])
@login_required
def project_year():
    """Filter projects, by project status and by start_date year"""
    db = get_db()

    years = db.query(extract('year', models.Project.start_date).distinct().label('year')).order_by('year').all()
    years = [year.year for year in years]

    year_filter = request.args.get('year', type=int)

    query = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"])

    if year_filter:
        query = query.filter(extract('year', models.Project.start_date) == year_filter)

    projects = query.order_by(models.Project.start_date.desc()).all()

    return render_template("portfolio/project_year.html", projects=projects, years=years, year_filter=year_filter)


@bp.route("/portfolio/datto", methods=['GET'])
@login_required
def datto():
    """Filter projects, by uploaded to datto and by start_date year"""
    db = get_db()

    years = db.query(extract('year', models.Project.start_date).distinct().label('year')).order_by('year').all()
    years = [year.year for year in years]

    datto_filter = request.args.get("datto")

    query = db.query(models.Project.id, models.Project.p_type, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.datto, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Project.invoice, models.Project.notes).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"])

    if datto_filter:#
        query = query.filter(models.Project.datto == datto_filter)

    projects = query.order_by(models.Project.start_date.desc()).all()

    return render_template("portfolio/datto.html", projects=projects, years=years)



@bp.route("/portfolio/project/<int:project_id>")
@login_required
def project_details(project_id):

    db = get_db()

    project = db.query(models.Project.p_type, models.Project.po_number, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.invoice, models.Project.datto, models.Project.notes, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Inspection.i_type2, models.Inspection.inspection_status2, models.Inspection.inspection_date2, models.Inspection.i_type3, models.Inspection.inspection_status3, models.Inspection.inspection_date3).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"], models.Project.id == project_id).distinct().all()

    return render_template("portfolio/project_details.html", project=project, project_id=project_id)


@bp.route("/portfolio/update/<int:project_id>", methods=("GET", "POST"))
@login_required
def update(project_id):
    """Update a post if the current user is the author."""

    if request.method == "POST":
        
        form_data = extract_form_data()
        error = validate_form_data(form_data)
        
        if error:
            flash(error, "danger")

            project_status = ["completed", "in_progress", "pending", "on_hold"]
            i_type = ["underground", "rough", "power_release", "final", "pending"]
            inspection_status = ["passed", "rescheduled", "pending"]
            p_type = ["dwp", "sce"]
            invoice = ["50%", "90%", "100%"]
            datto = ["completed", "in_progress", "pending"]

            return render_template("portfolio/update.html", project_status=project_status, i_type=i_type, inspection_status=inspection_status, p_type=p_type, invoice=invoice, datto=datto, project=[form_data], project_id=project_id)
    
        form_data = clean_form_data(form_data)

        db = get_db()
        project = db.query(models.Project).join(models.User, models.Project.user_id == models.User.id).filter(models.User.id == session["user_id"], models.Project.id == project_id).first()
        
        if project: 
            project.p_type = form_data["p_type"]
            project.po_number = form_data["po_number"]
            project.address = form_data["address"]
            project.num_chargers = form_data["num_chargers"]
            project.permit_num1 = form_data["permit_num1"]
            project.permit_num2 = form_data["permit_num2"]
            project.project_status = form_data["project_status"]
            project.start_date = form_data["start_date"]
            project.invoice = form_data["invoice"]
            project.datto = form_data["datto"]
            project.notes = form_data["notes"]
        
        inspection = db.query(models.Inspection).filter(models.Inspection.project_id == project.id).first()

        if inspection:
            inspection.i_type1 = form_data["i_type1"]
            inspection.inspection_status1 = form_data["inspection_status1"]
            inspection.inspection_date1 = form_data["inspection_date1"]
            inspection.i_type2 = form_data["i_type2"]
            inspection.inspection_status2 = form_data["inspection_status2"]
            inspection.inspection_date2 = form_data["inspection_date2"]
            inspection.i_type3 = form_data["i_type3"]
            inspection.inspection_status3 = form_data["inspection_status3"]
            inspection.inspection_date3 = form_data["inspection_date3"]
        
        db.commit()
        flash("Project Updated!", "primary")
        return redirect(url_for("portfolio.project_details", project_id=project.id))
    

    else:
        db = get_db()

        project = db.query(models.Project.p_type, models.Project.po_number, models.Project.address, models.Project.num_chargers, models.Project.permit_num1, models.Project.permit_num2, models.Project.project_status, models.Project.start_date, models.Project.invoice, models.Project.datto, models.Project.notes, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Inspection.i_type2, models.Inspection.inspection_status2, models.Inspection.inspection_date2, models.Inspection.i_type3, models.Inspection.inspection_status3, models.Inspection.inspection_date3).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"], models.Project.id == project_id).distinct().all()

           
        project_status = ["completed", "in_progress", "pending", "on_hold"]
        i_type = ["underground", "rough", "power_release", "final", "pending"]
        inspection_status = ["passed", "rescheduled", "pending"]
        p_type = ["dwp", "sce"]
        invoice = ["50%", "90%", "100%"]
        datto = ["completed", "in_progress", "pending"]

        return render_template("portfolio/update.html", project_status=project_status, i_type=i_type, inspection_status=inspection_status, p_type=p_type, invoice=invoice, datto=datto, project=project, project_id=project_id)



@bp.route("/portfolio/inspection", methods=['GET'])
@login_required
def inspection():
   
    db = get_db()

    inspection_status_filter = request.args.get("inspection_status1")

    query = db.query(models.Project.address, models.Project.permit_num1, models.Project.permit_num2, models.Inspection.i_type1, models.Inspection.inspection_status1, models.Inspection.inspection_date1, models.Inspection.i_type2, models.Inspection.inspection_status2, models.Inspection.inspection_date2, models.Inspection.i_type3, models.Inspection.inspection_status3, models.Inspection.inspection_date3).join(models.User, models.Project.user_id == models.User.id).join(models.Inspection, models.Project.id == models.Inspection.project_id).filter(models.User.id == session["user_id"])

    if project_status_filter:
        query = query.filter(models.Inspection.inspection_status1 == inspection_status_filter)

    projects = query.order_by(models.Inspection.inspection_date1.desc(), models.Inspection.inspection_date2.desc()).all()

    return render_template("portfolio/inspection.html", projects=projects)
