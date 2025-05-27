import argparse

from pathlib import Path


class ParseCSV:

    def __init__(
            self,
            *args: list,
            report: str | None = None,
            base_dir: Path = Path(__file__).resolve().parent.parent.parent / "data",
    ) -> None:
        self._data_files = args[0]
        self._report = report
        self._dict_data = {}
        self.base_dir = base_dir

    def parse_csv(self) -> None:
        '''Method for parse csv files to python dict'''

        for file in self._data_files:
            file_path = self.base_dir / file
            try:
                with open(file_path, "r") as f:
                    data = f.read()
                    data = data.split("\n")
                    data = [i.split(',') for i in data if i]

                    self._dict_data[file] = []
                    for i in data[1:]:
                        self._dict_data[file].append({data[0][indx]: i[indx] for indx in range(len(i))})

            except FileNotFoundError:
                print(f"File {self.base_dir / file[0]} not found")

    def _calculate_payout(self):
        '''Method for calculate payout and write it to dict'''

        for file, data in self._dict_data.items():
            for value in data:
                if salary := value.get("hourly_rate"):
                    salary = salary
                elif salary := value.get("rate"):
                    salary = salary
                elif salary := value.get("salary"):
                    salary = salary
                else:
                    raise ValueError("Not found salary")

                salary = int(salary)

                payout = int(value.get("hours_worked")) * salary
                value["payout"] = payout

    def _report_payout(self):
        '''Returning string report result'''
        self._calculate_payout()

        result = ""
        for file, value in self._dict_data.items():
            data = []
            department = set()
            for row in value:
                data.append(
                    ["", row["name"], row["hours_worked"], row["payout"], row["department"]]
                )
                department.add(row["department"])

            result += f"{file:=^80}\n"

            format_text = "{:<20} {:<30} {:<20} {:<20}"
            result += format_text.format(*["", "name", "hours_worked", "payout"]) + "\n"
            for dep in department:
                result += dep + "\n"
                hours_sum = 0
                payout_sum = 0
                for row in data:
                    if row[-1] == dep:
                        result += format_text.format(*row[:-1]) + "\n"
                        hours_sum += int(row[2])
                        payout_sum += int(row[3])
                result += format_text.format(*["", "", hours_sum, payout_sum]) + "\n"
            result += "=" * 80 + "\n"
        return result

    def get_result(self) -> str | None:
        '''Method for get result by report arg.
            Can extend in future'''

        if self._report == "payout":
            return self._report_payout()

    def __dict__(self) -> dict:
        '''Returning parsed csv files in dict'''
        return self._dict_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("data", nargs="+", type=str)
    parser.add_argument("--report", type=str, required=True)

    parse_args = parser.parse_args()

    parser_class = ParseCSV(parse_args.data, report=parse_args.report)
    parser_class.parse_csv()
    print(parser_class.get_result())
