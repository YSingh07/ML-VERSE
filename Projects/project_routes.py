from flask import Blueprint,render_template, request, redirect, url_for, flash ,session
from model.project_db import MLWiki
from database.database import db

project_bp=Blueprint("project_page",__name__,template_folder="templates",url_prefix="/project")

@project_bp.route("/admin")
def admin_project_info():
    wiki=[]
    return render_template("admin_project_info.html",username=session.get("username"),role=session.get("role"), wiki=wiki)









# Fields allowed to be updated through the form
WIKI_FIELDS = [
    "title",
    "slug",
    "image_path",
    "short_description",
    "about",
    "working",
    "model",
    "model_details",
    "preprocessing",
    "training",
    "evaluation",
    "usage",
    "dataset",
    "requirements",
    "pkl_file",
    "status",
]


# ==============================
# READ ALL WIKI ARTICLES
# ==============================

@project_bp.route("/wiki")
def wiki_list():

    wiki = MLWiki.query.order_by(
        MLWiki.last_updated.desc()
    ).all()

    return render_template(
        "Projects.html",
        project = wiki,
        username = session.get("username"),
        role = session.get("role")
    )


# ==============================
# CREATE WIKI ARTICLE
# ==============================

@project_bp.route("/wiki/add", methods=["GET", "POST"])
def wiki_add():

    if request.method == "POST":

        data = {
            field: request.form.get(field, "").strip()
            for field in WIKI_FIELDS
        }

        if not data["title"] or not data["slug"]:
            flash("Title and slug are required!", "danger")
            return render_template("wiki_form.html", wiki=None)

        existing_slug = MLWiki.query.filter_by(
            slug=data["slug"]
            ).first()

        if existing_slug:
            flash("Slug already exists!", "danger")
            return render_template("wiki_form.html", wiki=None)

        article = MLWiki(**data)

        db.session.add(article)
        db.session.commit()

        flash("Wiki article created successfully!", "success")

        return redirect(url_for("wiki_list"))

    return render_template("wiki_form.html", wiki=None)


# ==============================
# UPDATE WIKI ARTICLE
# ==============================

@project_bp.route("/wiki/edit/<int:wiki_id>", methods=["GET", "POST"])
def wiki_edit(wiki_id):

    article = MLWiki.query.get_or_404(wiki_id)

    if request.method == "POST":

        data = {
            field: request.form.get(field, "").strip()
            for field in WIKI_FIELDS
        }

        if not data["title"] or not data["slug"]:
            flash("Title and slug are required!", "danger")
            return render_template("wiki_form.html", wiki=article)

        existing_slug = MLWiki.query.filter(
            MLWiki.slug == data["slug"],
            MLWiki.id != article.id
        ).first()

        if existing_slug:
            flash("Slug already belongs to another article!", "danger")
            return render_template("wiki_form.html", wiki=article)

        for field, value in data.items():
            setattr(article, field, value)

        db.session.commit()

        flash("Wiki article updated successfully!", "success")

        return redirect(url_for("wiki_list"))

    return render_template("wiki_form.html", wiki=article)


# ==============================
# DELETE WIKI ARTICLE
# ==============================

@project_bp.route("/wiki/delete/<int:wiki_id>", methods=["POST"])
def wiki_delete(wiki_id):

    article = MLWiki.query.get_or_404(wiki_id)

    db.session.delete(article)
    db.session.commit()

    flash("Wiki article deleted successfully!", "success")

    return redirect(url_for("wiki_list"))
