from flask import Flask, request, render_template

import re
import functools
from datetime import datetime
from typing import List, Optional
import itertools


app = Flask(__name__)


@app.route(
    "/search/", methods=["GET"],
)
def search():
    """
    The endpoint scans cell towers and returns the result
    """
    date_now = datetime.now()
    cell_tower_ids: List[int] = request.args.getlist("cell_tower_id", type=int)
    phone_prefixes: List[str] = request.args.getlist("phone_prefix")
    protocols: List[str] = request.args.getlist("protocol")
    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None
    )
    try:
        date_from: Optional[datetime] = datetime.strptime(request.args.get("date_from"), '%Y%m%d')
        date_to: Optional[datetime] = datetime.strptime(request.args.get("date_to"), '%Y%m%d')

        if (date_from > date_now or date_to > date_now) or \
                (date_from.date() > date_to.date()):
            return "Incorrect date. Check for date", 400
    except TypeError as err:
        return f"Input second date. Description error => {err}", 400

    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    for tower in cell_tower_ids:
        if tower <= 0:
            return f"Tower value must be greater than zero", 400

    if phone_prefixes:
        for prefix in phone_prefixes:
            if re.findall(r'\d{3}[*]', prefix) or not len(re.findall(r'\d{10}', prefix)):
                return f"The phone number must be in 987* format or be no more than 10 digits long", 400
        # return f"You must specify at least one phone_prefixes", 400

    if protocols:
        for network in protocols:
            if network not in ["2G", "3G", "4G"]:
                return f"Incorrect network. Network should be 2G, 3G. 4G", 400
        # return f"You must specify at least one protocol", 400

    searches = {
        "cell_tower_ids": cell_tower_ids,
        "phone_prefixes": phone_prefixes,
        "protocols": protocols,
        "signal_level": signal_level,
        "date_from": date_from.date(),
        "date_to": date_to.date()
    }

    return render_template('get_request.html', searches=searches)


@app.route('/summ_digit/', methods=['GET'])
def summ_digit():
    """
    The endpoint accepts an array of numbers and returns the sum and multiplication
    """
    array_number: List[int] = request.args.getlist('numbers', type=int)

    return f"Full summ array: {sum(array_number)}\n" \
           f"Multiplication array {functools.reduce(lambda a, b: a * b, array_number)}"


@app.route('/nums_array/', methods=['GET'])
def num_pair_options():
    """

    example input: /nums_array/?array_1=1&array_1=2&array_1=3&array_2=5&array_2=6&array_2=7
    """
    one_array: List[int] = request.args.getlist('array_1', type=int)
    two_array: List[int] = request.args.getlist('array_2', type=int)
    result = [(a, b) for a in one_array for b in two_array]
    result_2 = list(itertools.product(one_array, two_array))
    return f"var_1 result - {result}" \
           f"var_2 with lib `itertools` - {result_2}"


@app.route('/min_size/', methods=['GET'])
def min_size():
    """
    example input: /min_size/?array=1&array=2&array=9&array=5&array=6&array=7&x_num=4
    """
    array: List[int] = request.args.getlist('array', type=int)
    x_num: int = request.args.get('x_num', type=int)
    result = min(array, key=lambda x: abs(x - x_num))

    return f"Min number to `{x_num}` from the array {array}: - <b>{result}</b>"


if __name__ == "__main__":
    app.run(debug=True)


# for search data:
# /search/?cell_tower_id=1&cell_tower_id=2&cell_tower_id=3&phone_prefix=999*&phone_prefix=921*&signal_level=-100
