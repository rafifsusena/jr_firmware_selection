'''
Writing rule :  variable, file name = snake_case
                constant = UPPER_CASE
                func/method = camelCase
                class = PascalCase
                string = double quote
                function gap = 2 blank line

2. Buat sebuah REST API dengan Flask dengan :
    - Port = 8080
    - Method = POST
    - Endpoint = /api/<nama kandidat>
    - Input = {"nilai": (nilai 0-100)} -> integer
    - Processing = 0-34:E; 35-49:D; 50-64:C; 65-79:B; 80-100:A
    - Processing = Invalid jika nilai tidak dalam 0-100, bukan angka dan key JSON tidak ada
    - Status nilai = A,B,C:lulus; D,E,Invalid:tidak lulus
    - Output = "nama": "(Nama Kandidat):, "nilai": "(nilai abjad)", "status": "(status nilai)"}
'''

from flask import Flask, request, jsonify

app = Flask(__name__)

NAMA_KANDIDAT = "rafif"
END_POINT = f"/api/{NAMA_KANDIDAT}"


@app.route(END_POINT, methods=["POST"])
def getResponse():
    data_receive = request.get_json()

    if not data_receive or "nilai" not in data_receive:
        return jsonify({"nama": NAMA_KANDIDAT, "nilai": "Invalid", "status": "tidak lulus"}), 400

    try:
        nilai_angka = int(data_receive["nilai"])
    except (ValueError, TypeError):
        return jsonify({"nama": NAMA_KANDIDAT, "nilai": "Invalid", "status": "tidak lulus"}), 400

    nilai_huruf = next(
        (huruf for batas, huruf in [
            (range(80, 101), "A"),
            (range(65, 80), "B"),
            (range(50, 65), "C"),
            (range(35, 50), "D"),
            (range(0, 35), "E"),
        ] if nilai_angka in batas),
        "Invalid"
    )

    status_lulus = "lulus" if nilai_huruf in ["A", "B", "C"] else "tidak lulus"

    return jsonify({"nama": NAMA_KANDIDAT, "nilai": nilai_huruf, "status": status_lulus}), 200


if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)