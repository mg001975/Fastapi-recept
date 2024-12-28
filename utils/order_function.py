from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import Step


# Assuming you have a Session configured
engine = create_engine("your_database_url")
Session = sessionmaker(bind=engine)
session = Session()


def reorder_steps(component_id, new_order):
    # Get the steps for the given component
    steps = session.query(Step).filter(Step.component_id == component_id).all()

    # Sort the steps based on the new_order array, assuming `new_order` is a list of step IDs in the desired order
    for index, step_id in enumerate(new_order):
        step = next(step for step in steps if step.id == step_id)
        step.order = (
            index + 1
        )  # New order value is the index + 1 (or any other logic you prefer)

    # Commit the changes to the database
    session.commit()

    return "Reorder Successful"
