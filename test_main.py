from services.db.services.admin_service import AdminServiceDB


admin = AdminServiceDB()


#admin.create_group(group_name="Администраторы")
#admin.create_user(tg_id=321, username="mktgts", fullname="qwewq", group_id=1)
#print(admin._return_group_id(user_id=2))
#print(admin.show_user_list())
#print(admin.show_group_list())
#admin.drop_user(user_id=4)
#admin.drop_group(group_id=1)
#admin.create_ticket(user_id=2, message="Test ticket")
#admin.create_operator(tg_id=2314, username="operator1", fullname="Operator Name", group_id=1)
#admin.create_admin(tg_id=4234242, username="admin1", fullname="Admin Name")