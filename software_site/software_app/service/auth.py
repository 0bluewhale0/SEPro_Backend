"""authentication service
"""
import hashlib
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist

from software_app.models import User, Pile, PileStatus, PileType
from software_app.service.exceptions import UserAlreadyExisted, UserDoesNotExisted, WrongPassword
from software_app.service.jwt_tools import Role, gen_token
from software_app.service.schd import Scheduler, scheduler
from software_app.config import CONFIG
from datetime import date

def register(username: str, password: str, key: str) -> None:
    """注册

    Args:
        username (str): 用户名
        password (str): 密码
        key (str): 注册码

    Raises:
        UserDoesNotExisted: 用户名不存在

    Returns:
        None
    """
    registered: User = User.objects.filter(username=username).exists()
    if registered:
        raise UserAlreadyExisted("用户名已被注册")
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if key in CONFIG['AuthCode']: # 注册为管理员
        user = User(username=username, password=hashed_password, is_admin=True)
    else: # 注册为普通用户
        user = User(username=username, password=hashed_password, is_admin=False)
    user.save()


def login(username: str, password: str) -> Tuple[str, Role]:
    """登陆

    Args:
        username (str): 用户名
        password (str): 密码

    Raises:
        UserDoesNotExisted: 用户名不存在
        WrongPassword: 密码错误

    Returns:
        Tuple[str, Role]: JWT令牌, 角色
    """
    try:
        user: User = User.objects.get(username=username)
    except ObjectDoesNotExist as e:
        raise UserDoesNotExisted("用户名不存在") from e
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()  # 原始密码是在加密之后再存储到数据库中的
    if user.password != hashed_password:
        raise WrongPassword("密码错误")
    role = Role.USER
    if user.is_admin:
        role = Role.ADMIN
    return gen_token(username, role.name), role


def init_pileModels() -> None:
    if CONFIG['cfg']['ForceApplyChange']==False:
        piles = Pile.objects.all()
        if len(piles) != 0: # pile数据库已经被初始化过了
            return
    else:
        
        TorF = input("是否强制应用Pile数据库更改？(y/n)")
        if TorF != 'y':
            return
    Pile.objects.all().delete()
    # pile数据库中没有数据，需要根据config文件去创建充电桩
    FastChargingPileNum = CONFIG['cfg']['FastChargingPileNum']
    TrickleChargingPileNum = CONFIG['cfg']['TrickleChargingPileNum']
    for i in range(FastChargingPileNum):
        Fpile = Pile.objects.create(pile_id = i+1, status=PileStatus.RUNNING, pile_type=PileType.FAST_CHARGE, register_time=date.today(), cumulative_charging_amount=0)
        Fpile.save()
    for i in range(TrickleChargingPileNum):
        Tpile = Pile.objects.create(pile_id = FastChargingPileNum+i+1, status=PileStatus.RUNNING, pile_type=PileType.CHARGE, register_time=date.today(), cumulative_charging_amount=0)
        Tpile.save()
    

if __name__=="main":...
    # init_pileModels()