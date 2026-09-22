import argparse
from .api import cancel_order, create_order, get_order


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("order_id")
    create.add_argument("customer")
    create.add_argument("total")
    show = sub.add_parser("get")
    show.add_argument("order_id")
    cancel = sub.add_parser("cancel")
    cancel.add_argument("order_id")
    args = parser.parse_args(argv)
    if args.command == "create":
        order = create_order(args.order_id, args.customer, args.total)
    elif args.command == "get":
        order = get_order(args.order_id)
    else:
        order = cancel_order(args.order_id)
    print(f"{order.order_id} {order.customer} {order.total} {order.status}")
    return 0


if __name__ == "__main__":
    main()
