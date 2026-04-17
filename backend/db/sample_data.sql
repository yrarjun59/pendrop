-- =====================================================
-- DML Script for Pendrop Database (Sample Data)
-- =====================================================

-- Clean existing data (optional)
DELETE FROM snapshots;
DELETE FROM chapters;
DELETE FROM books;
DELETE FROM journal_entries;

-- -----------------------------------------------------
-- 1. BOOKS (10 entries)
-- -----------------------------------------------------
INSERT INTO books (id, user_id, title, description) VALUES
('book-1', 'local-user', 'The Silent Garden', 'A novel about memory and loss'),
('book-2', 'local-user', 'Echoes of Tomorrow', 'Sci‑fi adventure set in 2147'),
('book-3', 'local-user', 'The Last Baker', 'A cozy mystery in a small town'),
('book-4', 'local-user', 'Unwritten Letters', 'Essays on love and distance'),
('book-5', 'local-user', 'Code & Poetry', 'Reflections on technology and art'),
('book-6', 'local-user', 'Mountain Pass', 'A memoir of hiking the Himalayas'),
('book-7', 'local-user', 'The Glass Cage', 'Thriller about a locked‑room mystery'),
('book-8', 'local-user', 'Recipes for Rainy Days', 'Cookbook with personal stories'),
('book-9', 'local-user', 'The Color of Sound', 'A musician''s journey'),
('book-10', 'local-user', 'Fragments of a Dream', 'Collection of short stories');

-- -----------------------------------------------------
-- 2. CHAPTERS (10 entries across different books)
-- -----------------------------------------------------
INSERT INTO chapters (id, book_id, chapter_number, title, content) VALUES
('ch1-1', 'book-1', 1, 'Prologue: The Gate', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The gate was rusted shut."}]}]}'),
('ch1-2', 'book-1', 2, 'The First Memory', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"I remember the garden before it went silent."}]}]}'),
('ch2-1', 'book-2', 1, 'Chapter 1: Last Train', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The monorail hissed into the station."}]}]}'),
('ch2-2', 'book-2', 2, 'Chapter 2: Echo', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"Her voice came from everywhere and nowhere."}]}]}'),
('ch3-1', 'book-3', 1, 'Chapter One: The Missing Dough', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"On Tuesday morning, the sourdough starter was gone."}]}]}'),
('ch3-2', 'book-3', 2, 'Chapter Two: A Suspicious Scone', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"Mrs. Albright always bought two scones."}]}]}'),
('ch4-1', 'book-4', 1, 'Distance', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"There are miles that cannot be measured."}]}]}'),
('ch5-1', 'book-5', 1, 'Syntax Error', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"I learned to code before I learned to write."}]}]}'),
('ch6-1', 'book-6', 1, 'Base Camp', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"At 5,364 meters, the air is thin and honest."}]}]}'),
('ch7-1', 'book-7', 1, 'The Invitation', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The envelope was sealed with black wax."}]}]}');

-- -----------------------------------------------------
-- 3. SNAPSHOTS (10 entries, manual backups of chapters)
-- -----------------------------------------------------
INSERT INTO snapshots (id, chapter_id, book_id, content_json, description) VALUES
('snap-1', 'ch1-1', 'book-1', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The gate was rusted shut."}]}]}', 'First draft of prologue'),
('snap-2', 'ch1-1', 'book-1', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The gate was rusted shut, and the lock had long since crumbled."}]}]}', 'Added detail about the lock'),
('snap-3', 'ch1-2', 'book-1', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"I remember the garden before it went silent. The roses used to hum."}]}]}', 'Expanded garden description'),
('snap-4', 'ch2-1', 'book-2', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The monorail hissed into the station. No one got off."}]}]}', 'First draft'),
('snap-5', 'ch2-2', 'book-2', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"Her voice came from everywhere and nowhere. It said my name."}]}]}', 'Added name reveal'),
('snap-6', 'ch3-1', 'book-3', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"On Tuesday morning, the sourdough starter was gone. So was the cat."}]}]}', 'Added missing cat'),
('snap-7', 'ch4-1', 'book-4', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"There are miles that cannot be measured. Like the space between two people in the same room."}]}]}', 'Complete thought'),
('snap-8', 'ch5-1', 'book-5', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"I learned to code before I learned to write. Maybe that explains the semicolons in my poems."}]}]}', 'Poetry metaphor'),
('snap-9', 'ch6-1', 'book-6', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"At 5,364 meters, the air is thin and honest. You cannot lie to yourself up here."}]}]}', 'Philosophical addition'),
('snap-10', 'ch7-1', 'book-7', '{"type":"doc","content":[{"type":"paragraph","content":[{"text":"The envelope was sealed with black wax. Inside, a single key."}]}]}', 'Added key');

-- -----------------------------------------------------
-- 4. JOURNAL ENTRIES (10 entries)
-- -----------------------------------------------------
INSERT INTO journal_entries (id, user_id, title, content, mood) VALUES
('journal-1', 'local-user', 'Morning thoughts', 'Woke up early today. The light was golden. Need to capture that feeling in the novel.', '🌅'),
('journal-2', 'local-user', 'Stuck on chapter 3', 'I can''t figure out why the baker would hide the dough. Motivation is weak.', '😤'),
('journal-3', 'local-user', 'Character idea', 'What if the antagonist is actually the protagonist from a different timeline?', '💡'),
('journal-4', 'local-user', NULL, 'Just wrote 2000 words. Exhausted but happy.', '😌'),
('journal-5', 'local-user', 'Research note', 'Monorail speeds in 2147: need to check physics. Or just make it up.', '🤓'),
('journal-6', 'local-user', 'Delete later', 'This is just a rant about noise. Feel better now.', '😶'),
('journal-7', 'local-user', 'Dream last night', 'I dreamed the garden was singing. Definitely using that.', '🌙'),
('journal-8', 'local-user', 'Progress', 'Chapter 5 is done! Time for a break.', '🎉'),
('journal-9', 'local-user', 'Idea for ending', 'The key opens a door that doesn''t exist. That''s the twist.', '🔑'),
('journal-10', 'local-user', NULL, 'Rainy day. Good for writing.', '☔');

-- Verify counts
SELECT 'Books' as table_name, COUNT(*) as row_count FROM books
UNION ALL
SELECT 'Chapters', COUNT(*) FROM chapters
UNION ALL
SELECT 'Snapshots', COUNT(*) FROM snapshots
UNION ALL
SELECT 'Journal', COUNT(*) FROM journal_entries;