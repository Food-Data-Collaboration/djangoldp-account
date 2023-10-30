def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['email'] = user.email
    claims['website'] = user.urlid
    claims['webid'] = user.urlid
    claims['preferred_username'] = user.username
    return claims

def sub_generator(user):
    return user.urlid
