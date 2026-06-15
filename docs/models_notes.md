# Models Explained - Blog Project

## First, what are we building?

We are building a Blog Website.

Features we want:

* Users can write blog posts.
* Posts can belong to categories.
* Users can comment on posts.
* Users can like posts.
* Each post should have tags.
* Each post should have a unique URL.

To support these features, we need database tables.

In Django, tables are created using Models.

---

# 1. Category Model

Question:

Suppose we create posts like:

Post 1 → Django Forms

Post 2 → Django Authentication

Post 3 → Python Basics

How do we group similar posts together?

Answer:

We create Categories.

Examples:

Django

Python

AI

Web Development

Therefore we created:

```python
class Category(models.Model):
```

Now every post can belong to one category.

Example:

Django Forms → Django Category

Python Basics → Python Category

---

## Why name field?

```python
name = models.CharField(max_length=100)
```

We need to store the category name.

Example:

"Django"

"Python"

"AI"

---

## Why slug field?

```python
slug = models.SlugField()
```

We want clean URLs.

Without slug:

```text
/category/1/
```

With slug:

```text
/category/django/
```

Much better.

---

# 2. Post Model

This is the most important model.

Question:

What is the main thing on a blog website?

Answer:

Blog Posts.

Therefore we created:

```python
class Post(models.Model):
```

Every article written by users will be stored here.

Example:

Title:
Learn Django Authentication

Content:
Long blog article...

Author:
Pratham

Category:
Django

---

## Why title?

```python
title = models.CharField()
```

Because every blog post needs a heading.

Example:

"Learn Django Authentication"

"Python for Beginners"

---

## Why content?

```python
content = RichTextField()
```

Because users need to write the article.

Example:

Paragraphs

Headings

Bold text

Images

Lists

Normal TextField would only give plain text.

RichTextField gives a proper editor.

---

## Why image?

```python
image = models.ImageField()
```

Most blogs show a thumbnail image.

Example:

A Django logo image at the top of the article.

---

# Understanding Foreign Keys

This is where many beginners get confused.

Think of a Foreign Key as:

"Connecting one table to another."

Example:

Category Table

| id | name   |
| -- | ------ |
| 1  | Django |
| 2  | Python |

Post Table

| id | title        | category |
| -- | ------------ | -------- |
| 1  | Django Forms | 1        |
| 2  | Django Auth  | 1        |

Notice:

The post does not store the word "Django".

It stores the category's ID.

This creates a connection.

This connection is called a Foreign Key.

---

## Why category ForeignKey?

```python
category = models.ForeignKey(Category)
```

Because every post should belong to a category.

Example:

Post:
"Django Forms"

Category:
"Django"

Without ForeignKey:

We would keep typing category names repeatedly.

With ForeignKey:

We simply connect the post to an existing category.

---

## Why author ForeignKey?

```python
author = models.ForeignKey(User)
```

Question:

Who wrote the post?

We need that information.

Example:

Post:
Django Forms

Author:
Pratham

Post:
Python Basics

Author:
Rahul

One User can write many Posts.

Therefore we connect Post to User.

---

# Understanding One-To-Many

User Table

| id | username |
| -- | -------- |
| 1  | Pratham  |

Post Table

| id | title         |
| -- | ------------- |
| 1  | Django Forms  |
| 2  | Django Auth   |
| 3  | Python Basics |

One user wrote many posts.

This is called:

One → Many

That is why we use ForeignKey.

---

# 3. Comment Model

Question:

How can visitors react to posts?

Answer:

Comments.

Therefore we created:

```python
class Comment(models.Model):
```

Example:

Post:
Django Forms

Comment:
Great article!

---

## Why post ForeignKey?

```python
post = models.ForeignKey(Post)
```

Because we need to know:

"This comment belongs to which post?"

Example:

Comment:
"Great article"

belongs to

Post:
"Django Forms"

---

## Why author ForeignKey?

```python
author = models.ForeignKey(User)
```

Because we need to know:

"Who wrote this comment?"

Example:

Comment:
Great article

Written by:
Rahul

---

# 4. Like Model

Question:

How can users like a post?

Answer:

Create a Like table.

Therefore:

```python
class Like(models.Model):
```

---

## Why not store likes directly in Post?

Bad approach:

```python
likes = 10
```

Now we know:

10 people liked.

But we don't know:

Who liked?

---

Better approach:

Create Like records.

Example:

| user    | post         |
| ------- | ------------ |
| Pratham | Django Forms |
| Rahul   | Django Forms |

Now we know exactly who liked what.

---

## Why user ForeignKey?

```python
user = models.ForeignKey(User)
```

Need to know:

Which user liked the post?

---

## Why post ForeignKey?

```python
post = models.ForeignKey(Post)
```

Need to know:

Which post was liked?

---

## Why unique_together?

```python
unique_together = ('post', 'user')
```

Suppose Pratham clicks Like 10 times.

Without this:

Database stores:

Pratham → Post 1

Pratham → Post 1

Pratham → Post 1

Pratham → Post 1

Wrong.

With unique_together:

Only one record allowed.

Pratham → Post 1

Correct.

---

# Final Relationships

User
|
|---- writes ----> Posts
|
|---- writes ----> Comments
|
|---- creates ---> Likes

Category
|
|---- contains --> Posts

Post
|
|---- has -------> Comments
|
|---- has -------> Likes

This structure gives us everything needed for a complete Blog Application.













# Profile Model Explained

## Why did we create this model?

Django already gives us a User model.

The User model contains basic information like:

* Username
* Email
* Password

Example:

| Username | Email                                 |
| -------- | ------------------------------------- |
| Pratham  | [abc@gmail.com](mailto:abc@gmail.com) |

But in a blog website we usually want more information about users.

For example:

* Bio
* Profile Picture
* Personal Website

The default Django User model does not have these fields.

Therefore we create a separate Profile model.

---

# Why not add these fields directly to User?

Django's User model is built-in.

Modifying it later can become complicated.

A common Django practice is:

Keep User as it is.

Create a Profile model and connect it to User.

---

# Understanding OneToOneField

```python
user = models.OneToOneField(User)
```

Think of it as:

One User → One Profile

Example:

| User    |
| ------- |
| Pratham |

↓

| Profile         |
| --------------- |
| Bio             |
| Profile Picture |
| Website         |

---

## Real Life Example

User Table

| id | username |
| -- | -------- |
| 1  | Pratham  |
| 2  | Rahul    |

Profile Table

| id | user_id | bio               |
| -- | ------- | ----------------- |
| 1  | 1       | Django Developer  |
| 2  | 2       | Python Enthusiast |

Notice:

Pratham has exactly one profile.

Rahul has exactly one profile.

This is called:

One User ↔ One Profile

Therefore we use:

```python
OneToOneField
```

and not

```python
ForeignKey
```

---

# Why user field?

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

Purpose:

Connect Profile to User.

Example:

User:
Pratham

Profile:
Bio: Django Developer

Now Django knows this profile belongs to Pratham.

---

# What does on_delete=models.CASCADE mean?

Suppose:

User:
Pratham

Profile:
Pratham's Profile

If Pratham's account is deleted,

Should the profile remain?

No.

The profile becomes useless.

Therefore:

```python
on_delete=models.CASCADE
```

means:

Delete the profile automatically when the user is deleted.

---

# Why bio?

```python
bio = models.TextField(blank=True)
```

Purpose:

Allow users to write about themselves.

Example:

"I am a final year IT student interested in Django and AI."

We use TextField because bios can be longer than normal text.

---

# What does blank=True mean?

Users are not forced to enter a bio.

Example:

Valid:

Bio = "I love Python"

Also Valid:

Bio = Empty

---

# Why profile_picture?

```python
profile_picture = models.ImageField(...)
```

Purpose:

Allow users to upload a profile image.

Example:

Instead of showing:

Pratham

We can show:

👤 Pratham's photo

---

## upload_to='profile_pics/'

```python
upload_to='profile_pics/'
```

When users upload images, Django stores them inside:

```text
media/
    profile_pics/
```

Example:

```text
media/
    profile_pics/
        pratham.jpg
```

This keeps profile images organized.

---

# Why blank=True and null=True?

```python
blank=True
null=True
```

Purpose:

Profile picture is optional.

A user can create an account even without uploading a photo.

Example:

Pratham → Has photo

Rahul → No photo

Both are allowed.

---

# Why website?

```python
website = models.URLField(blank=True)
```

Purpose:

Allow users to share their personal website.

Examples:

https://pratham.dev

https://github.com/pratham

https://linkedin.com/in/pratham

Django validates that it looks like a proper URL.

---

# Why **str** method?

```python
def __str__(self):
    return f'{self.user.username} Profile'
```

Without this:

Django Admin shows:

```text
Profile object (1)
```

Not very helpful.

With **str**:

```text
Pratham Profile
```

Much easier to identify.

---

# Final Flow

User registers
↓
User account created
↓
Profile created automatically
↓
User adds:
- Bio
- Profile Picture
- Website
↓
Profile information displayed on blog website

---

# Relationship Summary

User
│
└── Profile

One User → One Profile

This is why we use OneToOneField instead of ForeignKey.
