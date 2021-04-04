from sqlalchemy.orm import Session
from pydantic import EmailStr

from users import models as users_models
from access_control import models as ac_models
from config.db import Base
from utils.users import get_password_hash



def init_db(db: Session, email: EmailStr, password: str):
    user_dict = {
        'email': email,
        'firstname': 'Super',
        'lastname': 'Admin',
        'password_hash': get_password_hash(password)
    }
    perms = ['can_create_permission', 'can_view_permission', 'can_modify_permission', 'can_delete_permission']
    role_perms = ['can_create_role', 'can_view_role', 'can_modify_role', 'can_delete_role']
    group_perms = ['can_create_group', 'can_view_group', 'can_modify_group', 'can_delete_group']
    perm_admin = ac_models.Role(name='permission_admin')
    role_admin = ac_models.Role(name='role_admin')
    group_admin = ac_models.Role(name='group_admin')

    for perm_name in perms:
        perm = ac_models.Permission(name=perm_name)
        perm_admin.permissions.append(perm)
        db.add(perm)
    for perm_name in role_perms:
        perm = ac_models.Permission(name=perm_name)
        role_admin.permissions.append(perm)
        db.add(perm)
    for perm_name in group_perms:
        perm = ac_models.Permission(name=perm_name)
        group_admin.permissions.append(perm)
        db.add(perm)

    super_admin_group = ac_models.Group(name='super_admin_group')
    super_admin_group.roles.append(perm_admin)
    super_admin_group.roles.append(role_admin)
    super_admin_group.roles.append(group_admin)
    user = users_models.User(**user_dict)
    user.groups.append(super_admin_group)
    db.add_all([perm_admin, role_admin, group_admin, super_admin_group, user])
    db.commit()