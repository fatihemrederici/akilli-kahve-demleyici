import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi değişkenleri
coffee_type = ctrl.Antecedent(np.arange(0, 3, 1), 'coffee_type')  # 0: Espresso, 1: Filter, 2: Turkish
intensity = ctrl.Antecedent(np.arange(0, 11, 1), 'intensity')      # 0-10 arası
room_temp = ctrl.Antecedent(np.arange(10, 36, 1), 'room_temp')     # 10-35 °C
water_temp = ctrl.Antecedent(np.arange(60, 101, 1), 'water_temp')  # 60-100 °C
coffee_amount = ctrl.Antecedent(np.arange(5, 31, 1), 'coffee_amount') # 5-30 gram

# Çıkış değişkenleri
brew_time = ctrl.Consequent(np.arange(0, 121, 1), 'brew_time')     # 0-120 saniye
flow_rate = ctrl.Consequent(np.arange(0, 21, 1), 'flow_rate')      # 0-20 ml/s

# Üyelik fonksiyonları
coffee_type['espresso'] = fuzz.trimf(coffee_type.universe, [0, 0, 1])
coffee_type['filter'] = fuzz.trimf(coffee_type.universe, [0, 1, 2])
coffee_type['turkish'] = fuzz.trimf(coffee_type.universe, [1, 2, 2])

# Diğer değişkenlerde otomatik üyelik fonksiyonları
intensity.automf(3)    # 'poor', 'average', 'good'
room_temp.automf(3)
water_temp.automf(3)
coffee_amount.automf(3)

brew_time.automf(3)    # 'poor', 'average', 'good'
flow_rate.automf(3)

# Kurallar
rules = [
    ctrl.Rule(intensity['good'] & coffee_amount['good'], brew_time['good']),
    ctrl.Rule(water_temp['good'] & room_temp['good'], flow_rate['poor']),
    ctrl.Rule(coffee_type['turkish'], brew_time['poor']),
    ctrl.Rule(coffee_type['turkish'], flow_rate['poor']),
    ctrl.Rule(intensity['average'] & coffee_amount['average'], brew_time['average']),
    ctrl.Rule(coffee_amount['poor'] & intensity['poor'], brew_time['poor']),
    ctrl.Rule(water_temp['poor'], flow_rate['good']),
]

# Kontrol sistemi oluşturma
brewing_ctrl = ctrl.ControlSystem(rules)
brewing_simulator = ctrl.ControlSystemSimulation(brewing_ctrl)

def simulate(inputs):
    for key, value in inputs.items():
        brewing_simulator.input[key] = value
    brewing_simulator.compute()
    return brewing_simulator.output['brew_time'], brewing_simulator.output['flow_rate']
