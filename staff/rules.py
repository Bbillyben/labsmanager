from .models import Employee, Employee_Superior
import rules
from settings.models import LabsManagerSetting

#    Predicates ======================
@rules.predicate
def is_user_employee(user, employee = None):
    """ return true if the employee instance is the current linked user employee
    """
    if not employee:
        return False
    return (employee.user == user) & user.has_perm("common.self_edit")

@rules.predicate
def is_user_subordinate(user, employee = None):
    if not employee:
        return False
    try:
        sup = Employee.objects.get(user=user)
    except:
        return False
    setting =LabsManagerSetting.get_setting('EMPLOYEE_CAN_EDIT_SUBORDINATE')
    if setting:
        return Employee_Superior.is_in_superior_hierarchy(sup, employee)
    else:
        return False
    
@rules.predicate
def is_team_leader(user, team= None):
    """ return true if the user's employee instance is the team leader
    """
    if not team:
        return False
    try:
        sup = Employee.objects.get(user=user)
    except:
        return False
    
    return team.leader == sup

@rules.predicate
def is_participant_manager(user, part= None):
    if not part:
        return False
    proj_right = user.has_perm("project.change_project", part.project)
    emp_right = user.has_perm("staff.change_employee", part.employee)
    return proj_right & emp_right

#    Rules ======================
rules.add_perm('staff.change_employee', is_user_employee |  is_user_subordinate)
rules.add_perm('staff.add_genericinfo', is_user_employee |  is_user_subordinate)
rules.add_perm('staff.change_genericinfo', is_user_employee |  is_user_subordinate)

rules.add_perm('staff.change_team', is_team_leader)

rules.add_perm('staff.change_participant', is_participant_manager)


