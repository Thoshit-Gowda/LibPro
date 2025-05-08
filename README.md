# 📚 Library Management System – Database Schema

This document outlines the structure and constraints of the tables used in the **Library Management System** database.

---

## 📦 Inventory Table

Tracks individual copies of books using SKU numbers.

```sql
CREATE TABLE Inventory (
    SKUNumber VARCHAR(50) PRIMARY KEY,
    ISBN VARCHAR(13) NOT NULL CHECK (CHAR_LENGTH(ISBN) = 10 OR CHAR_LENGTH(ISBN) = 13),
    Status VARCHAR(100) NOT NULL CHECK (
        Status IN ('Shelved', 'Unshelved', 'Missing', 'Damaged', 'Borrowed', 'Lost')
    ),
    BorrowedBy VARCHAR(255),
    Category VARCHAR(100) CHECK (Category != ''),
    BayNumber INT CHECK (BayNumber >= 0),
    ShelfNumber INT CHECK (ShelfNumber >= 0),
    RowNumber INT CHECK (RowNumber >= 0),
    ColumnNumber INT CHECK (ColumnNumber >= 0),
    AddedOn DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Fields:

* `SKUNumber`: Unique identifier for each book copy.
* `ISBN`: Links to a book in the `Books` table.
* `Status`: Current status of the book copy.
* `BorrowedBy`: Email of the member (if borrowed).
* `Category`, `BayNumber`, `ShelfNumber`, `RowNumber`, `ColumnNumber`: Physical location.
* `AddedOn`, `UpdatedOn`: Timestamps for tracking changes.

---

## 📘 Books Table

Contains metadata for each unique book.

```sql
CREATE TABLE Books (
    BookNumber INT NOT NULL UNIQUE AUTO_INCREMENT,
    ISBN VARCHAR(13) PRIMARY KEY CHECK (CHAR_LENGTH(ISBN) = 10 OR CHAR_LENGTH(ISBN) = 13),
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Author VARCHAR(100) NOT NULL,
    Publication VARCHAR(100) NOT NULL,
    Genre VARCHAR(100) NOT NULL,
    Language VARCHAR(50) NOT NULL,
    DateAdded DATETIME DEFAULT CURRENT_TIMESTAMP,
    LastUpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Fields:

* `ISBN`: Primary key and reference for all book copies.
* `BookNumber`: Unique incremental ID.
* Includes `Title`, `Author`, `Publication`, `Genre`, and `Language`.

---

## 👥 Members Table

Stores information about registered library members.

```sql
CREATE TABLE Members (
    MemberNumber INT NOT NULL UNIQUE AUTO_INCREMENT,
    EmailID VARCHAR(255) PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    MobileNumber CHAR(10) CHECK (
        MobileNumber BETWEEN '1000000000' AND '9999999999'
    ),       
    WishlistedBooks TEXT,       
    Points INT DEFAULT 0 CHECK (Points >= 0),
    BooksHistory TEXT,         
    Fines DECIMAL(10,2) DEFAULT 0.00 CHECK (Fines >= 0),
    DateOfJoining DATETIME DEFAULT CURRENT_TIMESTAMP,
    LastLoginOn DATETIME DEFAULT NULL,
    LastUpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Fields:

* `EmailID`: Primary key.
* `Password`: Encrypted string.
* `MobileNumber`: Must be a valid 10-digit number.
* `Points`, `Fines`: For gamification and penalties.
* `WishlistedBooks`, `BooksHistory`: Stored as serialized text.

---

## 🧑‍🏫 Librarian Table

Manages staff-level users of the system.

```sql
CREATE TABLE Librarian (
    LibrarianNumber INT NOT NULL UNIQUE AUTO_INCREMENT,
    EmailID VARCHAR(255) PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    MobileNumber CHAR(10) UNIQUE CHECK (
        MobileNumber BETWEEN '1000000000' AND '9999999999'
    ),
    DateOfJoining DATETIME DEFAULT CURRENT_TIMESTAMP,
    LastLoginOn DATETIME DEFAULT NULL,
    LastUpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Fields:

* Similar to `Members`, but for administrative access.
* `MobileNumber` is unique.

---

## ✍️ Reviews Table

Stores book reviews submitted by members or readers.

```sql
CREATE TABLE Reviews (
    ReviewID INT NOT NULL UNIQUE AUTO_INCREMENT,
    ISBN VARCHAR(13) PRIMARY KEY,
    ReviewerName VARCHAR(100) NOT NULL,
    ReviewerEmail VARCHAR(255) NOT NULL,
    Rating INT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Review TEXT NOT NULL,
    ReviewedOn DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Fields:

* `ISBN`: Tied to a book (should ideally allow multiple reviews per book — see note below).
* `Rating`: 1 to 5 stars.
* `ReviewerName`, `ReviewerEmail`: Reviewer identity.

---

## 📄 BooksRecord Table

Logs borrow/return/lost transactions of books.

```sql
CREATE TABLE BooksRecord (
    RecordNumber INT NOT NULL AUTO_INCREMENT UNIQUE,
    SKU VARCHAR(50) PRIMARY KEY,
    Status ENUM('Borrowed', 'Returned', 'Lost') NOT NULL,
    ISBN VARCHAR(13) NOT NULL,
    Email VARCHAR(255),
    FullName VARCHAR(100),
    Points INT DEFAULT 0 CHECK (Points >= 0),
    DaysBorrowed INT DEFAULT 0 CHECK (DaysBorrowed >= 0),
    DaysLate INT DEFAULT 0 CHECK (DaysLate >= 0),
    Fine DECIMAL(10,2) DEFAULT 0.00 CHECK (Fine >= 0),
    DueOn DATE,
    ReturnedOn DATE,
    UpdatedOn DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CreatedOn DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Fields:

* Tracks lifecycle of a book’s lending status.
* `SKU`: Unique to a physical copy (used as primary key).
* `Points`, `Fine`, `DaysLate`: Useful for reward/penalty systems.
