from services.db.services.admin_service import AdminServiceDB


admin = AdminServiceDB()

admin.create_user(tg_id=23, username="qstepashka", fullname="qstepan", group_id=1)
print(admin._return_group_id(user_id=2))