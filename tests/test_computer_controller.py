from aura.computer.controller import ComputerController


def test_computer_controller_rejects_unknown_action():

    controller = ComputerController()

    result = controller.execute_action(
        "unknown",
    )

    assert "Unsupported" in result


def test_computer_controller_blocks_unknown_application():

    controller = ComputerController()

    result = controller.execute_action(
        "open:unknown_app",
    )

    assert "Blocked" in result
