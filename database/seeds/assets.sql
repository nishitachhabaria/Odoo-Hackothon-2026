-- AssetFlow asset seed examples.
-- Replace UUID placeholders with actual category and department ids before running.
-- These are seed examples only.

INSERT INTO assets (
    id,
    asset_tag,
    name,
    description,
    category_id,
    department_id,
    serial_number,
    manufacturer,
    model_number,
    purchase_date,
    purchase_cost,
    warranty_expiry,
    condition,
    location,
    status,
    is_bookable,
    photo_url,
    document_url,
    created_by,
    updated_by,
    created_at,
    updated_at
)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'AF-000001', 'Laptop', 'AssetFlow example laptop', '00000000-0000-0000-0000-000000000001', NULL, 'SN-LAP-0001', 'Dell', 'Latitude 5440', '2026-01-15', 1200.00, '2027-01-15', 'Good', 'Head Office', 'Available', FALSE, '/uploads/assets/laptop.png', '/uploads/assets/laptop.pdf', NULL, NULL, NOW(), NOW()),
    ('11111111-1111-1111-1111-111111111112', 'AF-000002', 'Desktop', 'AssetFlow example desktop', '00000000-0000-0000-0000-000000000001', NULL, 'SN-DESK-0001', 'HP', 'EliteDesk 800', '2026-01-20', 950.00, '2027-01-20', 'Good', 'Operations Floor', 'Available', FALSE, '/uploads/assets/desktop.png', '/uploads/assets/desktop.pdf', NULL, NULL, NOW(), NOW()),
    ('11111111-1111-1111-1111-111111111113', 'AF-000003', 'Projector', 'AssetFlow example projector', '00000000-0000-0000-0000-000000000002', NULL, 'SN-PROJ-0001', 'Epson', 'EB-X06', '2026-02-01', 650.00, '2027-02-01', 'Excellent', 'Conference Room', 'Available', TRUE, '/uploads/assets/projector.png', '/uploads/assets/projector.pdf', NULL, NULL, NOW(), NOW()),
    ('11111111-1111-1111-1111-111111111114', 'AF-000004', 'Meeting Room', 'AssetFlow example meeting room resource', '00000000-0000-0000-0000-000000000003', NULL, 'SN-MEET-0001', 'AssetFlow', 'MR-01', '2026-02-10', 0.00, '2027-02-10', 'Good', 'Building A', 'Available', TRUE, '/uploads/assets/meeting-room.png', '/uploads/assets/meeting-room.pdf', NULL, NULL, NOW(), NOW()),
    ('11111111-1111-1111-1111-111111111115', 'AF-000005', 'Vehicle', 'AssetFlow example vehicle', '00000000-0000-0000-0000-000000000004', NULL, 'SN-VEH-0001', 'Toyota', 'Corolla', '2026-03-05', 15000.00, '2027-03-05', 'Excellent', 'Parking Bay 1', 'Available', FALSE, '/uploads/assets/vehicle.png', '/uploads/assets/vehicle.pdf', NULL, NULL, NOW(), NOW()),
    ('11111111-1111-1111-1111-111111111116', 'AF-000006', 'Printer', 'AssetFlow example printer', '00000000-0000-0000-0000-000000000005', NULL, 'SN-PRN-0001', 'Canon', 'iR-ADV C3530', '2026-03-15', 800.00, '2027-03-15', 'Good', 'IT Department', 'Available', TRUE, '/uploads/assets/printer.png', '/uploads/assets/printer.pdf', NULL, NULL, NOW(), NOW());
