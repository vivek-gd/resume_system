import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Resume, ResumeHistory

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("✓ Tables created successfully")

    print("\nChecking Resume model...")
    print(f"  - name: {Resume.name.type}")
    print(f"  - job: {Resume.job.type}")
    print(f"  - intro: {Resume.intro.type}")
    print(f"  - phone: {Resume.phone.type}")
    print(f"  - email: {Resume.email.type}")
    print(f"  - education: {Resume.education.type}")
    print(f"  - experience: {Resume.experience.type}")
    print(f"  - skills: {Resume.skills.type}")
    print(f"  - certificates: {Resume.certificates.type}")
    print(f"  - avatar: {Resume.avatar.type}")
    print(f"  - update_time: {Resume.update_time.type}")

    print("\nChecking ResumeHistory model...")
    print(f"  - old_name: {ResumeHistory.old_name.type}")
    print(f"  - old_job: {ResumeHistory.old_job.type}")
    print(f"  - old_intro: {ResumeHistory.old_intro.type}")
    print(f"  - old_phone: {ResumeHistory.old_phone.type}")
    print(f"  - old_email: {ResumeHistory.old_email.type}")
    print(f"  - old_education: {ResumeHistory.old_education.type}")
    print(f"  - old_experience: {ResumeHistory.old_experience.type}")
    print(f"  - old_skills: {ResumeHistory.old_skills.type}")
    print(f"  - old_certificates: {ResumeHistory.old_certificates.type}")
    print(f"  - old_avatar: {ResumeHistory.old_avatar.type}")

    print("\n✓ All checks passed!")
    print("\nDatabase is ready. You can now start the application.")
