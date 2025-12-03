import circuitydatabase as circuity
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    default_csv_url = "https://storage.googleapis.com/espn-data/espn-nfl-rosters.csv"
    query = ""

    example_queries = [
                       "trevor lawrence age",
                       "arizona cardinals wide receiver name",
                       "cardinals receiver name years of experience",
    ]

    headers = None
    rows = None

    database = circuity.initialize_database()
    database = circuity.import_comma_separated_values(database, default_csv_url)
    column_names = database["column_names"]

    if request.method == "POST":
        csv_url = request.form.get("csvUrl") or default_csv_url
        query = request.form.get("query")

        database = circuity.initialize_database()
        database = circuity.import_comma_separated_values(database, csv_url)
        column_names = database["column_names"]        

        try:
            results = circuity.process_query(database, query)
            merged_results_dictionary = {
                                         key: [str(dict[key]) for dict in results]
                                         for key in results[0]
            }
            result_values_matrix = circuity.transpose_matrix(list(merged_results_dictionary.values()))
        
            headers = list(merged_results_dictionary.keys())
            rows = result_values_matrix
        except:
            headers = ["Error"]
            rows = [["no matches found"]]

    return render_template(
        "base.html",
        default_csv_url = default_csv_url,
        query = query,
        headers = headers,
        rows = rows,
        column_names = column_names,
        example_queries = example_queries,
    )


if __name__ == "__main__":
    app.run(debug=True)

