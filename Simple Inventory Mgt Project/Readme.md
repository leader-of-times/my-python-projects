# Inventory Management System

## Overview

This project is an Inventory Management System designed to handle various CRUD operations for managing products and user purchases. It includes functionalities for both admins and users to interact with the system. The system supports:

- Viewing, adding, updating, and deleting products.
- Searching products by name or category.
- Purchasing products and generating purchase reports.

## Features

### Admin Features

1. **Display All Products**: View all products with their details or categorized by type.
2. **Display Specific Product**: View details of a specific product by its ID.
3. **Add New Product**: Insert a new product into the inventory.
4. **Update Product**: Modify the details of an existing product.
5. **Delete Product**: Remove a product from the inventory.
6. **Display User Purchase Reports**: View detailed reports of user purchases.

### User Features

1. **Search Product by Name**: Find products by their name.
2. **Search Product by Category**: Find products by their category.
3. **Purchase Product**: Buy products and generate a bill.

## Technologies Used

- **Python 3.x**: Programming language used for developing the application.
- **JSON**: Data format for storing product and user information.
- **Tabulate**: Library used for pretty-printing tables of data in the console.
- **pytest**: Framework for writing and running tests for the application.

## Setup and Usage

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   ```

2. Navigate to the project directory:
   ```bash
   cd inventory-management-system
   ```

3. Install the required Python packages:
   ```bash
   pip install tabulate pytest
   ```

### Running the Application

To run the application, execute the `project.py` script:

```bash
python project.py
```

### Testing

To run the tests, ensure that `pytest` is installed and run the following command:

```bash
pytest
```

### Test Coverage

The following functionalities are tested:

- **Displaying Data**: Verify that all products are displayed correctly.
- **Displaying Specific Product**: Ensure the correct product details are shown for a given ID.
- **Adding New Product**: Check that new products are added to the database correctly.
- **Deleting Product**: Confirm that products are removed from the database as expected.
- **Updating Product Data**: Test updating various attributes of a product.
- **Displaying Reports**: Validate that user purchase reports are displayed correctly.
- **Searching Products**: Test searching for products by name and category.
- **Purchasing Products**: Verify the purchasing process and bill generation.

## File Structure

- `project.py`: Main script containing the application logic.
- `data.json`: File used to store product information.
- `user_data.json`: File used to store user purchase data.
- `test_project.py`: File containing tests for the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have improvements or bug fixes.
