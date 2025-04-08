from services.db.services.admin_service import AdminServiceDB


admin = AdminServiceDB()


#admin.create_group(group_name="Новострой")
#admin.create_user(tg_id=423423, username="Cxzc", fullname="Jjkhnm", user_type=2 ,group_id=2)
#print(admin._return_group_id(user_id=2))
#print(admin.show_user_list())
#print(admin.show_group_list())
#admin.drop_user(user_id=2)
#admin.drop_group(group_id=1)
admin.create_ticket(
    user_id=2,
    group_id=2,
    operator_id=1,
    message="Test ticket",
    )