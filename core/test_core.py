import logging
import typer

from os.path import join
from engine import Engine

def find():
    typer.echo("Loading ...")
    engine = Engine()
    engine.load()
    typer.echo("Loaded")
    while True:
        query = input("Enter a query: ")
        documents = engine.find(query)
        for document in documents:
            typer.echo(
                f"Id: {document.id}, "
                + f"Relevancy: {document.relevancy}, "
                + f"Title: {document.title}",
            )

def load():
    engine = Engine()
    engine.load()
    typer.echo("Loaded")


def save(data: str):
    typer.echo("Loading ...")
    engine = Engine()
    engine.train(data)
    typer.echo("Loaded")
    engine.save()

def save_all():
    save("data/all_data.json")

def save_cisi():
    save("data/cisi_data.json")

def save_cran():
    save("data/cran_data.json")

def test(data: str, query: str, top: int = 10):
    typer.echo("Loading ...")
    engine = Engine()
    engine.train(data)
    typer.echo("Loaded")
    typer.echo("Running Precision test ...")
    print(engine.find("What problems and concerns are there in making up descriptive titles? What difficulties are involved in automatically retrieving articles from approximate titles? What is the usual relevance of the content of articles to their titles?"))
    # precision = engine.test_precision(query, top)
    # typer.echo(f"Precision: {precision}")
    # typer.echo("Running Recall test ...")
    # recall = engine.test_recall(query, top)
    # typer.echo(f"Recall: {recall}")
    # typer.echo("Running F test ...")
    # f = engine.test_f(precision=precision, recall=recall)
    # typer.echo(f"F: {f}")
    # typer.echo("Running Fallout test ...")
    # fallout = engine.test_recall(query, top)
    # typer.echo(f"Fallout: {fallout}")

def test_all(top: int = 10):
    test("data/all_data.json", "data/all_query.json", top)


def test_cisi(top: int = 10):
    test("data/cisi_data.json", "data/cisi_query.json", top)

def test_cran(top: int = 10):
    test("data/cran_data.json", "data/cran_query.json", top)

if __name__ == "__main__":
    test_cran()