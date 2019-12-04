import requests
import arrow
import numpy as np
from tabulate import tabulate


def main():
    SERVER_NAME = "ecotype-42"

    START_DATE = "2019-04-12T10:00:00"
    END_DATE = "2019-04-12T11:00:00"

    start_epoch = arrow.get(START_DATE).timestamp
    end_epoch = arrow.get(END_DATE).timestamp

    sensors = requests.get("https://api.seduce.fr/servers/all/sensors").json()
    [server_sensors] = [sensor for sensor in sensors if sensor.get("name") == SERVER_NAME]

    front_temperature_data = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('temp').get('front')}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    back_temperature_data = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('temp').get('back')}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    power_consumption_pdu1_data = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('power')[0]}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    power_consumption_pdu2_data = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('power')[1]}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()

    # Detect timestamps that may be missing in the data returned for pdu1 or pdu2
    all_timestamps = power_consumption_pdu1_data.get("epoch_ts") + power_consumption_pdu2_data.get("epoch_ts")
    missing_timestamps = [ts for ts in all_timestamps if ts not in power_consumption_pdu1_data.get("epoch_ts")]
    missing_timestamps += [ts for ts in all_timestamps if ts not in power_consumption_pdu2_data.get("epoch_ts")]

    pdu1_power_consumptions = [value
                               for (ts, value) in zip(power_consumption_pdu1_data.get("epoch_ts"), power_consumption_pdu1_data.get("values"))
                               if ts not in missing_timestamps]
    pdu2_power_consumptions = [value
                               for (ts, value) in zip(power_consumption_pdu2_data.get("epoch_ts"), power_consumption_pdu2_data.get("values"))
                               if ts not in missing_timestamps]

    cumulated_consumptions = [pdu1_cons + pdu2_cons
                              for (pdu1_cons, pdu2_cons) in zip(pdu1_power_consumptions, pdu2_power_consumptions)]

    front_temperatures = front_temperature_data.get("values")
    back_temperatures = back_temperature_data.get("values")

    results = [
        ["", "cumulated power (W)", "front temp. (C)", "back temp. (C)"],
        ["mean", np.mean(cumulated_consumptions), np.mean(front_temperatures), np.mean(back_temperatures)],
        ["min", np.min(cumulated_consumptions), np.min(front_temperatures), np.min(back_temperatures)],
        ["max", np.max(cumulated_consumptions), np.max(front_temperatures), np.max(back_temperatures)],
    ]

    print(tabulate(results))


if __name__ == "__main__":
    main()
