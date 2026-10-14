#!/usr/bin/env python3
"""Generates demo data for the Quora app into seed/out (Mongo and Elasticsearch NDJSON, Postgres SQL).

The run is deterministic: the same seed always produces the same ids and text, so reloading is idempotent.
"""
import json
import os
import random
from datetime import datetime, timedelta, timezone

from knowledge import java, sql, spring
from knowledge import platform as infra

SEED = 20261014
ANCHOR = datetime(2026, 10, 14, 6, 0, 0, tzinfo=timezone.utc)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
USER_COUNT = 500

rng = random.Random(SEED)

# ---------------------------------------------------------------- text templates

CONCEPT_ANGLES = [
    ("What {be} {n}{s}?", "define"),
    ("How {does} {n} work{s}?", "define"),
    ("When should I use {n}{s}?", "usage"),
    ("What are common mistakes with {n}{s}?", "pitfall"),
    ("Can someone explain {n} with an example{s}?", "define"),
    ("{Be} {n} a good idea{s}?", "usage"),
    ("Best practices for {n}{s}", "usage"),
    ("Interview question: explain {n}{s}", "define"),
    ("Why do people say to be careful with {n}{s}?", "pitfall"),
    ("What problem {does} {n} solve{s}?", "usage"),
    ("{N} explained simply{s}", "define"),
    ("What should I know about {n}{s} before using it?", "pitfall"),
]
PAIR_ANGLES = [
    ("What is the difference between {a} and {b}{s}?", "diff"),
    ("{A} vs {b}: which one should I use{s}?", "rule"),
    ("When to use {a} instead of {b}{s}?", "rule"),
    ("Difference between {a} and {b}: interview question{s}", "diff"),
    ("Should I choose {a} or {b}{s}?", "rule"),
    ("{A} or {b}: how do I decide{s}?", "rule"),
    ("Why would anyone use {b} over {a}{s}?", "b"),
    ("Explain {a} versus {b} with an example{s}", "diff"),
]
HOWTO_ANGLES = [
    ("How do I {t}{s}?", 0),
    ("What is the best way to {t}{s}?", 1),
    ("How can I {t}{s}?", 2),
    ("Simple way to {t}{s}", 0),
    ("{T}: how to do it properly{s}", 1),
    ("Can't figure out how to {t}{s}", 2),
    ("How to {t}{s}: recommended approach?", 1),
    ("Is there a cleaner way to {t}{s}?", 0),
]
ERROR_ANGLES = [
    ('Why do I get "{e}"{s}?', 0),
    ('How to fix "{e}"{s}', 1),
    ('"{E}": what does it mean{s}?', 2),
    ('Getting "{e}", what is the cause{s}?', 0),
    ('What causes "{e}"{s}?', 1),
    ('"{E}" suddenly appearing{s}', 2),
    ('Help with "{e}"{s}', 0),
]

INTROS = [
    "I'm fairly new to {T} and still building my mental model.",
    "We ran into this in our project last week.",
    "I'm preparing for a backend interview and this keeps coming up.",
    "I inherited a codebase that relies on this.",
    "I read the official docs but it still isn't clear.",
    "A teammate raised this during code review.",
    "I'm building a side project and want to get this right from the start.",
    "This came up while debugging a production issue.",
]
CLOSINGS = ["", "", "Examples would be appreciated.", "Any pointers or links are welcome.", "Thanks in advance!"]
CONCEPT_ASKS = [
    "Could someone explain {n}, including when to use it and what to watch out for?",
    "What is the right way to think about {n}?",
    "I'd like to understand {n} well enough to explain it to my team.",
    "What are the trade-offs of {n}?",
    "Can you share a practical example of {n}?",
]
PAIR_ASKS = [
    "What are the real differences between {a} and {b}, and how do I choose?",
    "When is {a} the better option and when is {b}?",
    "Is there a simple rule for picking between {a} and {b}?",
    "Can someone compare {a} and {b} with a short example?",
]
HOWTO_ASKS = [
    "What is the cleanest way to {t}?",
    "I'd like to {t} without extra dependencies if possible.",
    "What is the recommended approach to {t}?",
    "How would you {t} in a real project?",
]
ERROR_ASKS = [
    'I keep seeing "{e}". What causes it and how do I fix it?',
    'My application fails with "{e}". Where should I start looking?',
    'What does "{e}" mean and what is the usual fix?',
]

OPENERS = ["", "", "Short answer: ", "Quick rundown. ", "From experience: ", "Here is how I see it. "]
CLOSERS = ["", "", "", " Hope this helps.", " Check the official documentation for version-specific details.", " Happy to share an example if that would help."]
GOTCHA_PREFIXES = ["Keep in mind: ", "One caveat: ", "The usual gotcha: "]

GENERIC_COMMENTS = [
    "Thanks, this cleared it up for me.",
    "This worked for me, much appreciated.",
    "Could you add a short code example?",
    "Does this still apply in newer versions?",
    "Good explanation, upvoted.",
    "Clear and to the point.",
    "I ran into exactly this last week, thanks.",
    "Can you share the source for this?",
    "This should be the accepted answer.",
]
FACT_COMMENTS = ["Worth adding: {x}", "One more thing to note: {x}", "Small addition: {x}"]
REPLIES = [
    "Good point, thanks.",
    "Agreed, that matches what I saw.",
    "Glad it helped!",
    "Yes, that's right.",
    "Thanks for the correction.",
    "I'll try that and report back.",
    "Makes sense now.",
]

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Ishaan", "Kabir", "Vihaan", "Ananya", "Diya", "Meera", "Priya",
    "Saanvi", "Kavya", "Neha", "Riya", "Sneha", "Pooja", "Rahul", "Amit", "Karthik", "Sanjay", "Deepak", "Nikhil",
    "Siddharth", "Varun", "Harsh", "Manish", "Emma", "Liam", "Olivia", "Noah", "Sophia", "Lucas", "Mia", "Ethan",
    "Ava", "Mason", "Chloe", "Daniel", "Zoe", "Mateo", "Lena", "Yuki", "Wei", "Fatima", "Omar", "Nadia", "Ivan", "Sara",
]
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Patel", "Reddy", "Iyer", "Nair", "Mehta", "Kapoor", "Joshi", "Das", "Bose",
    "Rao", "Kulkarni", "Malhotra", "Chopra", "Khan", "Smith", "Johnson", "Brown", "Garcia", "Miller", "Davis",
    "Martinez", "Lopez", "Wilson", "Anderson", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Kim", "Nguyen",
    "Tanaka", "Silva", "Costa", "Rossi", "Muller", "Novak", "Kowalski", "Haddad", "Cohen", "Okafor", "Mensah",
]

# ---------------------------------------------------------------- helpers

_proc = "".join(rng.choice("0123456789abcdef") for _ in range(10))
_counter = rng.randrange(0xFFFFFF)


def new_id(ts):
    global _counter
    _counter = (_counter + 1) & 0xFFFFFF
    return f"{int(ts.timestamp()):08x}{_proc}{_counter:06x}"


def date(ts):
    return {"$date": ts.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ts.microsecond // 1000:03d}Z"}


def after(ts, mean_hours, floor_minutes=2):
    delta = timedelta(minutes=floor_minutes) + timedelta(hours=rng.expovariate(1 / mean_hours))
    return min(ts + delta, ANCHOR - timedelta(minutes=1))


def cap(s):
    return s[0].upper() + s[1:]


def is_plural(name):
    # lowercase s only, so SQL keywords such as EXISTS stay singular
    head = name.split(" in ")[0]
    return " and " in name or (head.endswith("s") and not head.endswith("ss"))


def dump(f, obj):
    f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")


def sql_str(s):
    return "'" + s.replace("'", "''") + "'"


# ---------------------------------------------------------------- question variants

def build_variants(topic):
    suffixes = topic["suffixes"]
    variants = []
    for item in topic["concepts"]:
        for tmpl, kind in CONCEPT_ANGLES:
            variants += [("concept", item, tmpl, kind, s) for s in suffixes]
    for item in topic["pairs"]:
        for tmpl, kind in PAIR_ANGLES:
            variants += [("pair", item, tmpl, kind, s) for s in suffixes]
    for item in topic["howtos"]:
        for tmpl, kind in HOWTO_ANGLES:
            variants += [("howto", item, tmpl, kind, s) for s in suffixes]
    for item in topic["errors"]:
        for tmpl, kind in ERROR_ANGLES:
            variants += [("error", item, tmpl, kind, s) for s in suffixes]
    return variants


def make_title(family, item, tmpl, s):
    if family == "concept":
        plural = is_plural(item[0])
        return tmpl.format(n=item[0], N=cap(item[0]), s=s, be="are" if plural else "is",
                           Be="Are" if plural else "Is", does="do" if plural else "does")
    if family == "pair":
        return tmpl.format(a=item[0], b=item[1], A=cap(item[0]), s=s)
    if family == "howto":
        return tmpl.format(t=item[0], T=cap(item[0]), s=s)
    return tmpl.format(e=item[0], E=cap(item[0]), s=s)


def make_body(topic, family, item):
    intro = rng.choice(INTROS).format(T=topic["name"])
    if family == "concept":
        ask = rng.choice(CONCEPT_ASKS).format(n=item[0])
    elif family == "pair":
        ask = rng.choice(PAIR_ASKS).format(a=item[0], b=item[1])
    elif family == "howto":
        ask = rng.choice(HOWTO_ASKS).format(t=item[0])
    else:
        ask = rng.choice(ERROR_ASKS).format(e=item[0])
    return " ".join(x for x in (intro, ask, rng.choice(CLOSINGS)) if x)


def question_tags(topic, family, item, title):
    extra = {"howto": "how-to", "error": "troubleshooting", "pair": "comparison"}.get(family)
    tags = list(topic["tags"]) + list(item[-1]) + ([extra] if extra else [])
    if title.startswith("Interview"):
        tags.append("interview")
    seen, result = set(), []
    for t in tags:
        t = t.lower()
        if t not in seen and len(t) <= 30:
            seen.add(t)
            result.append(t)
    return result[:5]


# ---------------------------------------------------------------- answers

def concept_answer(item, kind, k, base):
    _, d, u, p, _ = item
    facts = {"d": d, "u": u, "p": p}
    order = {"define": "dup", "usage": "udp", "pitfall": "pud"}[kind]
    if k > 0:
        order = order[k % 3:] + order[:k % 3]
    keys = order[: (3 if k % 2 == 0 else 2)]
    fmt = (k + base) % 3
    labels = {"d": "What it is", "u": "When to use it", "p": "Watch out for"}
    if fmt == 2:
        return "\n".join(f"- {labels[x]}: {facts[x]}" for x in keys)
    parts = [(rng.choice(GOTCHA_PREFIXES) + facts[x]) if x == "p" else facts[x] for x in keys]
    if fmt == 1:
        return "\n\n".join(parts) + rng.choice(CLOSERS)
    return rng.choice(OPENERS) + " ".join(parts) + rng.choice(CLOSERS)


def pair_answer(item, kind, k, base):
    a, b, af, bf, rule, _ = item
    first, second = (a, af), (b, bf)
    if kind == "b" or k % 4 == 3:
        first, second = second, first
    fmt = (k + base) % 3
    if fmt == 0:
        return f"{first[0]}: {first[1]} {second[0]}: {second[1]} In short: {rule}"
    if fmt == 1:
        return f"- {first[0]}: {first[1]}\n- {second[0]}: {second[1]}\n\nRule of thumb: {rule}"
    return f"{first[1]} {second[1]}\n\nMy rule of thumb: {rule}" + rng.choice(CLOSERS)


def howto_answer(item, k, base):
    _, solution, code, _ = item
    fmt = (k + base) % 3
    if fmt == 0:
        return f"{solution}\n\nExample:\n{code}"
    if fmt == 1:
        return f"{code}\n\n{solution}" + rng.choice(CLOSERS)
    return f"Here is a simple way. {solution}\n\n{code}"


def error_answer(item, k, base):
    _, cause, fix, _ = item
    fmt = (k + base) % 3
    if fmt == 0:
        return f"This is usually caused by {cause}. To fix it, {fix}."
    if fmt == 1:
        return f"Cause: {cause}.\n\nFix: {cap(fix)}."
    return f"I hit the same thing. It was caused by {cause}. What worked for me: {fix}." + rng.choice(CLOSERS)


def make_answer(family, item, kind, k, base):
    if family == "concept":
        text = concept_answer(item, kind, k, base)
    elif family == "pair":
        text = pair_answer(item, kind, k, base)
    elif family == "howto":
        text = howto_answer(item, k, base)
    else:
        text = error_answer(item, k, base)
    assert 10 <= len(text) <= 1000, (family, item[0], len(text))
    return text


def extra_fact(family, item):
    index = {"concept": 3, "pair": 4, "howto": 1, "error": 2}[family]
    return item[index]


# ---------------------------------------------------------------- main generation

def main():
    os.makedirs(OUT, exist_ok=True)
    topics = list(java.TOPICS) + list(sql.TOPICS) + list(spring.TOPICS) + list(infra.TOPICS)

    files = {name: open(os.path.join(OUT, name), "w", encoding="utf-8") for name in (
        "tags.ndjson", "questions.ndjson", "answers.ndjson", "comments.ndjson", "likes.ndjson", "es_questions.ndjson")}
    counts = dict.fromkeys(("questions", "answers", "comments", "likes"), 0)
    all_tags = set()
    seen_titles = set()

    def write_likes(target_id, target_type, target_ts, n):
        for _ in range(n):
            ts = after(target_ts, 24 * 5)
            dump(files["likes.ndjson"], {
                "_id": {"$oid": new_id(ts)}, "targetId": target_id, "targetType": target_type,
                "liked": rng.random() > 0.1, "createdAt": date(ts)})
            counts["likes"] += 1

    def write_comment(content, target_id, target_type, ts):
        cid = new_id(ts)
        dump(files["comments.ndjson"], {
            "_id": {"$oid": cid}, "content": content, "targetId": target_id, "targetType": target_type,
            "createdAt": date(ts), "updatedAt": date(ts)})
        counts["comments"] += 1
        if rng.random() < 0.4:
            write_likes(cid, "COMMENT", ts, rng.choice([1, 1, 2, 3, 4]))
        return cid

    def write_comment_tree(answer_id, answer_ts, extra):
        for _ in range(rng.choices([0, 1, 2, 3, 4, 5], weights=[42, 25, 15, 10, 5, 3])[0]):
            ts = after(answer_ts, 20)
            text = rng.choice(GENERIC_COMMENTS) if rng.random() < 0.55 else rng.choice(FACT_COMMENTS).format(x=extra)
            cid = write_comment(text, answer_id, "ANSWER", ts)
            if rng.random() < 0.3:
                parent_id, parent_ts = cid, ts
                for _ in range(rng.choice([1, 1, 2])):
                    rts = after(parent_ts, 8)
                    rid = write_comment(rng.choice(REPLIES), parent_id, "COMMENT", rts)
                    if rng.random() < 0.1:
                        write_comment(rng.choice(REPLIES), rid, "COMMENT", after(rts, 4))
                    parent_id, parent_ts = (rid, rts) if rng.random() < 0.3 else (parent_id, parent_ts)

    for topic in topics:
        variants = build_variants(topic)
        rng.shuffle(variants)
        made = 0
        for family, item, tmpl, kind, suffix in variants:
            if made >= topic["count"]:
                break
            title = make_title(family, item, tmpl, suffix)
            if not 10 <= len(title) <= 100 or title.lower() in seen_titles:
                continue
            if suffix and suffix.split()[-1].lower() in title.replace(suffix, "").lower():
                continue
            seen_titles.add(title.lower())
            made += 1

            q_ts = ANCHOR - timedelta(hours=1) - timedelta(days=540 * rng.random() ** 1.4)
            qid = new_id(q_ts)
            body = make_body(topic, family, item)
            tags = question_tags(topic, family, item, title)
            all_tags.update(tags)

            q_likes = max(0, min(250, int(rng.paretovariate(1.5) * 2) - rng.randrange(0, 4)))
            n_answers = rng.choices(range(7), weights=[6, 24, 26, 20, 12, 7, 5])[0]
            views = min(250000, max(int(rng.lognormvariate(5.0, 1.2)), q_likes * 6 + n_answers * 10))

            dump(files["questions.ndjson"], {
                "_id": {"$oid": qid}, "title": title, "content": body, "tags": tags, "views": views,
                "createdAt": date(q_ts), "updatedAt": date(q_ts)})
            dump(files["es_questions.ndjson"], {"index": {"_index": "questions", "_id": qid}})
            dump(files["es_questions.ndjson"], {"title": title, "content": body})
            counts["questions"] += 1
            write_likes(qid, "QUESTION", q_ts, q_likes)

            extra = extra_fact(family, item)
            base = rng.randrange(3)
            used = set()
            for k in range(n_answers):
                text = make_answer(family, item, kind, k, base)
                for _ in range(10):
                    if text not in used:
                        break
                    text = rng.choice(OPENERS[2:]) + make_answer(family, item, kind, k, base)
                if text in used:
                    continue
                used.add(text)
                a_ts = after(q_ts, 36)
                aid = new_id(a_ts)
                dump(files["answers.ndjson"], {
                    "_id": {"$oid": aid}, "content": text, "questionId": qid,
                    "createdAt": date(a_ts), "updatedAt": date(a_ts)})
                counts["answers"] += 1
                scale = 2.0 if k == 0 else 1.2
                write_likes(aid, "ANSWER", a_ts,
                            max(0, min(200, int(rng.paretovariate(1.6) * scale) - rng.randrange(0, 3))))
                write_comment_tree(aid, a_ts, extra)
        print(f"{topic['name']:<14} {made} questions")

    for tag in sorted(all_tags):
        # no _id: the loader upserts by name so tags that already exist keep their ids
        dump(files["tags.ndjson"], {"name": tag, "createdAt": date(ANCHOR - timedelta(days=560))})
    for f in files.values():
        f.close()

    # users go to PostgreSQL
    used, rows = set(), []
    while len(rows) < USER_COUNT:
        first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        username = f"{first}.{last}".lower()
        if username in used:
            username += str(rng.randrange(10, 99))
        if username in used:
            continue
        used.add(username)
        created = ANCHOR - timedelta(days=rng.randint(30, 800), minutes=rng.randint(0, 1440))
        rows.append(f"({sql_str(username)}, {sql_str(username + '@example.com')}, "
                    f"{sql_str(first + ' ' + last)}, '{created:%Y-%m-%d %H:%M:%S}')")
    with open(os.path.join(OUT, "users.sql"), "w", encoding="utf-8") as f:
        for i in range(0, len(rows), 100):
            f.write("INSERT INTO users (username, email, display_name, created_at) VALUES\n")
            f.write(",\n".join(rows[i:i + 100]))
            f.write("\nON CONFLICT DO NOTHING;\n")

    print(f"tags {len(all_tags)}, users {USER_COUNT}, " + ", ".join(f"{k} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
