SET NAMES utf8mb4;
USE app_db;

CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prix DECIMAL(6,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

INSERT INTO produits (nom, prix, stock) VALUES
    ('Clavier mécanique', 59.90, 34),
    ('Souris sans fil', 24.50, 120),
    ('Écran 24 pouces', 139.00, 18);
