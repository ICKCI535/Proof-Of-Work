import requests
import json
from datetime import datetime


def get_raw_data(date):  # format: 2022-10-01
    url = f"https://therundown.io/api/v1/sports/11/openers/{date}?include=all_periods&key=HpBWyn01b5EpWPssdMeGh4INE1cYGP&offset=-420"
    r = requests.get(url)
    return json.loads(r.text)


def process_data(result, event_id=None):  # event_id got from TheRunDownConsumer.sol
    if event_id:
        output_json = {}
        for event in result["events"]:
            if event["event_id"] == event_id:
                output_json["event_id"] = event["event_id"]
                time_started = datetime.fromisoformat(
                    event["event_date"].replace("Z", "") + "+00:00").timestamp()
                output_json["event_date"] = int(time_started)
                output_json["event_status"] = event["score"]["event_status"]
                output_json["score_home"] = event["score"]["score_home"]
                output_json["score_away"] = event["score"]["score_away"]
                output_json["home_name"] = event["teams"][0]["name"]
                output_json["away_name"] = event["teams"][1]["name"]
                for i in range(1, 30):
                    if not event["line_periods"][f"{i}"]:
                        continue
                    output_json["point_spread_home"] = str(
                        event["line_periods"][f'{i}']["period_full_game"]["spread"]["point_spread_home"])
                    spread = str(
                        float(output_json["point_spread_home"])).split('.')
                    if spread[1] == "75" or spread[1] == "25" or spread[1] == "0":
                        spread = float(spread[0]+"."+"5")
                        output_json["point_spread_home"] = spread
                    output_json["total_over"] = str(
                        event["line_periods"][f'{i}']["period_full_game"]["total"]["total_over"])
                    if float(output_json["total_over"]) > 0.1:
                        print(i)
                        break
                # output_json["teams_normalized"] = event["teams_normalized"]

        return {"data": output_json}
    else:
        output = []
        for event in result["events"]:
            output_json = {}
            output_json["event_id"] = event["event_id"]
            time_started = datetime.fromisoformat(
                event["event_date"].replace("Z", "") + "+00:00").timestamp()
            output_json["event_date"] = int(time_started)
            output_json["event_status"] = event["score"]["event_status"]
            output_json["score_home"] = event["score"]["score_home"]
            output_json["score_away"] = event["score"]["score_away"]
            output_json["home_name"] = event["teams"][0]["name"]
            output_json["away_name"] = event["teams"][1]["name"]

            for i in range(1, 30):
                if not event["line_periods"][f"{i}"]:
                    continue
                output_json["point_spread_home"] = str(
                    event["line_periods"][f'{i}']["period_full_game"]["spread"]["point_spread_home"])
                print(str(output_json["point_spread_home"]))
                spread = str(
                    float(output_json["point_spread_home"])).split('.')
                if spread[1] == "75" or spread[1] == "25" or spread[1] == "0":
                    spread = float(spread[0]+"."+"5")
                    output_json["point_spread_home"] = spread
                output_json["total_over"] = str(
                    event["line_periods"][f'{i}']["period_full_game"]["total"]["total_over"])
                if float(output_json["total_over"]) > 0.1:
                    # print(str(output_json["total_over"]))
                    total = str(float(output_json["total_over"])).split('.')
                    if total[1] == "75" or total[1] == "25" or total[1] == "0":
                        total = float(total[0]+"."+"5")
                        output_json["total_over"] = total
                    break
            output.append(output_json)
        return {"data": output}


def write_to_file(output):
    with open("scripts/python/therundown/result.json", "w") as f:
        f.write(json.dumps(output))


if __name__ == "__main__":
    result = get_raw_data("2022-10-23")
    # output = process_data(result, "9ded75dbfd129c52db8813e3349647c6")
    output = process_data(result)
    write_to_file(output)
