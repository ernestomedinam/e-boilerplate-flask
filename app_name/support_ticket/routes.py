from flask import Blueprint, make_response, request, jsonify
from app_name.support_ticket.models import BasicSupportTicket

support_ticket_module = Blueprint("support_ticket", __name__)

@support_ticket_module.route("/support-tickets", methods=["GET", "POST"])
@support_ticket_module.route("/support-tickets/<int:ticket_id>", methods=["PUT"])
def handle_support_tickets(ticket_id = None):
    """
        handle support tickets endpoint requests:
            GET:    /support-tickets: list of all open tickets
            POST:   /support-tickets: create a new ticket from nametag
            PUT:    /support-tickets/<ticket_id>: close a ticket for given id
    """
    headers = {
        "Content-Type": "application/json"
    }
    response = {
        "status_code": 404,
        "text": ""
    }
    if request.headers.get("Content-Type") == headers["Content-Type"]:
        if request.method == "GET":
            tickets = BasicSupportTicket.query.filter_by(status="open").all()
            response["text"] = [ticket.serialize() for ticket in tickets]
            response["status_code"] = 200
        elif request.method == "POST":
            input_data = request.json
            if (
                "nametag" in input_data and
                isinstance(input_data["nametag"], str) and
                len(input_data["nametag"]) > 2
            ):
                new_ticket = BasicSupportTicket.create(input_data.pop("nametag"))
                if isinstance(new_ticket, BasicSupportTicket):
                    response["text"] = new_ticket.serialize()
                    response["status_code"] = 201
                else:
                    response = new_ticket
            else:
                response["text"] = "need a nametag type string at least 3 char long..."
                response["status_code"] = 400
        elif request.method == "PUT":
            ticket = BasicSupportTicket.query.filter_by(
                id=ticket_id,
                status="open"
            ).one_or_none()
            if ticket is not None:
                closed = ticket.close()
                if closed == True:
                    response["text"] = ticket.serialize()
                    response["status_code"] = 200
                else:
                    response = closed
            else:
                response["text"] = "no such item..."
    else:
        response["text"] = "wrong content type on headers..."
        response["status_code"] = 400

    return make_response(
        jsonify(response["text"]),
        response["status_code"],
        headers
    )