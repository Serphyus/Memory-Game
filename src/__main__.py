from app import App


if __name__ == "__main__":
    app = App(
        title="Memory-Game",
        resolution=(600, 600),
        board_size=[4, 4],
        field_spacing=10,
        font_size=30
    )

    app.run()