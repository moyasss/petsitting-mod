from sims4.tuning.instance_manager import InstanceManager
from sims4.tuning.tunable import TunableFactory
from sims4 import commands
import services
import alarms
from date_and_time import create_time_span
from sims.sim_info import SimInfo

def start_pet_sitting(sim_info, hours=3, pay_per_hour=25):
    total_earned = hours * pay_per_hour
    sim_info.household.funds.add(total_earned, Consts_pb2.TELEMETRY_MONEY_REASONS_SCRIPT)
    sim_info.add_buff_from_op('buff_Happy')
    print(f"{sim_info.first_name} earned §{total_earned} for pet sitting!")

@commands.Command('start.petsit', command_type=commands.CommandType.Live)
def run_pet_sitting(_connection=None):
    output = commands.CheatOutput(_connection)
    sim_info = services.get_active_sim_info()
    if not sim_info.is_teen:
        output("❌ Only teen Sims can pet sit!")
        return
    output("🐾 You started pet sitting! You’ll get paid in 3 hours.")

    # Wait 3 in-game hours, then pay
    def on_alarm(_):
        start_pet_sitting(sim_info)

    alarm_service = alarms.add_alarm(
        sim_info,
        create_time_span(hours=3),
        on_alarm,
        repeating=False
    )
