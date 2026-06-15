from src.infra.factory import ApplicationFactory


def main() -> None:
    app = ApplicationFactory.create()
    app.run()


if __name__ == "__main__":
    main()
