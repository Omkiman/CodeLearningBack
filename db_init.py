from models import db, CodeBlock

def init_database(app):
    """Initialize the database and populate it with sample data if empty"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Populate with sample data if database is empty
        if CodeBlock.query.count() == 0:
            codeblocks = [
                CodeBlock(
                    name="Hello World",
                    template="const hello_world = () => {\n  // your code here}",
                    solution="const hello_world = () => {\n  console.log('Hello, world!');}",
                    explanation="This is a simple function that logs 'Hello, world!' to the console."
                ),
                CodeBlock(
                    name = "Sort Array",
                    template = "function sortArray(arr) {\n  // your code here\n}",
                    solution = "function sortArray(arr) {\n  return arr.sort((a, b) => a - b);\n}",
                    explanation = "Sorts an array of numbers in ascending order using the built-in sort method."
                ),
                CodeBlock(
                    name = "Filter Even Numbers",
                    template = "function filterEven(arr) {\n  // your code here\n}",
                    solution = "function filterEven(arr) {\n  return arr.filter(num => num % 2 === 0);\n}",
                    explanation = "Returns only the even numbers from the given array."
                ),
                CodeBlock(
                    name = "Multiply n by m",
                    template =  "function multiply(n, m) {\n  // your code here\n}",
                    solution = "function multiply(n, m) {\n  return n * m;\n}",
                    explanation = "A simple function that multiplies two numbers and returns the result."
                )
            ]
            db.session.bulk_save_objects(codeblocks)
            db.session.commit()
            print("Database initialized with sample data")
        else:
            print("Database already contains data - skipping initialization")