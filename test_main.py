from services.db.services.admin_service import AdminServiceDB
import json


admin = AdminServiceDB()

print(admin._return_info_on_inn(inn=123))


#admin.create_group(group_name="Администраторы")
#admin.create_user(tg_id=321, username="mktgts", fullname="qwewq", group_id=1)
#print(admin._return_group_id(user_id=2))
#print(admin.show_user_list())
#print(admin.show_group_list())
#admin.drop_user(user_id=4)
#admin.drop_group(group_id=1)
#admin.create_ticket(user_id=1, message="threeth ticket")
#admin.create_operator(tg_id=123, username="operator1", fullname="maksim", group_id=1)
#admin.create_admin(tg_id=427431420, username="odintsovav", fullname="Александр")
#admin.edit_user_ip(user_id=1, user_ip='192.168.1.10')
#admin.edit_user_geo(user_id=1, user_geo="серверная")
#admin.drop_ticket(ticket_id=1)
#print(admin.user_ticket_list(user_id=1))
#print(admin.user_registration(invite_token=7996322, tg_id=6542, username="User1", fullname="User1 Name"))
#print(admin.show_groups_users(operator_id=1))
#admin.edit_status(ticket_id=1, status="in work")
#print(admin._in_base(3211))
#print(admin._in_invite(765874))
#print(admin._return_user_id(321))
#print(admin._return_group_operator(group_id=1))
#print(admin._check_role(tg_id=987421065))
#admin.create_admin(tg_id=987421065, username="mktgts", fullname="Максим")
#print(admin.show_user_list_by_group_id(groupd_id=1))
#print(admin.show_ticket_list_for_admin(group_id=1))


'''admin.create_group(
    group_name=admin._return_info_on_inn(inn=370260905156)["suggestions"][0]["value"],
    inn="370260905156"
)'''

#print(admin._return_admins_id_list())


#print(admin._have_fullname(tg_id=987421065))

#
#print(admin.show_groups_users(tg_id=2314))
#print(admin.show_ticket_list_for_operator(tg_id=987421065))

#print(admin._return_user_info(tg_id=987421065).fullname)
#print(admin._return_operator_info(group_id=2).fullname)
#print(admin._return_group_info(group_id=2).group_name)
#print(admin._return_company_name(inn=3328423228))
'''
def for_test():
    admin.create_admin(tg_id=987421065, username="mktgts", fullname="Maksim")
    admin.create_user(tg_id=123, username="user1", fullname="User Name", group_id=1)
    admin.create_user(tg_id=9789, username="secon_user", fullname="Name User2", group_id=1)
    admin.create_user(tg_id=5435, username="threeth_user", fullname="Threeth User", group_id=1)
    admin.create_operator(tg_id=2314, username="operator1", fullname="Operator Name", group_id=1)
    admin.create_group(group_name="Группа1")
    admin.create_ticket(user_id=2, message="Первый тикет")'''

#for_test()

#print(admin._all_user_tg_id_list())


#print(admin.show_operators_list())
#print(admin._return_info_on_inn(inn="370260905156"))

#print(json.dumps({"asd":"sad", "asds":"eqw"}, ensure_ascii=False, indent=4))
for i in (json.dumps(d, ensure_ascii=False, indent=4) for d in admin.show_ticket_list_for_admin()):
    print(i)

#print([type(d) for d in admin.show_ticket_list_for_admin()])




