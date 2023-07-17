-- Kreiranje baze podataka
CREATE DATABASE car_service_db;

-- Korišćenje baze podataka
USE car_service_db;

-- Tabela "user" (korisnik)
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);

-- Tabela "customers" (kupci)
CREATE TABLE customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  address VARCHAR(255),
  phone VARCHAR(20)
);

-- Tabela "service" (usluge)
CREATE TABLE service (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL
);

-- Tabela "vehicles" (vozila)
CREATE TABLE vehicles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT,
  make VARCHAR(255) NOT NULL,
  model VARCHAR(255) NOT NULL,
  year VARCHAR(255) NOT NULL,
  year INT,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Tabela "appointments" (termini)
CREATE TABLE appointments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT,
  vehicle_id INT,
  service_id INT,
  appointment_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
  FOREIGN KEY (service_id) REFERENCES service(id)
);
