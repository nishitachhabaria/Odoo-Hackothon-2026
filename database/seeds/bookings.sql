-- Seed a sample resource booking for Meeting Room A.
-- Replace booked_by with a valid user UUID if necessary.

INSERT INTO resource_bookings (
    id,
    asset_id,
    booked_by,
    department_id,
    title,
    description,
    start_datetime,
    end_datetime,
    status,
    created_at,
    updated_at
)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    '11111111-1111-1111-1111-111111111114',
    '33333333-3333-3333-3333-333333333333',
    NULL,
    'Meeting Room A Reservation',
    'Reserved meeting room for team planning',
    NOW() + INTERVAL '1 day' + INTERVAL '9 hour',
    NOW() + INTERVAL '1 day' + INTERVAL '10 hour',
    'Upcoming',
    NOW(),
    NOW()
);
