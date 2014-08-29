#!/usr/bin/env python
import requests
import argparse
import json

def print_result(res):
	for k, v in res.items():
		print("{:>20}: {:<80}".format(k, v))

def create(args):
	name, domain = args.email.split('@')
	res = requests.post(args.server + 'mail/account/', data=json.dumps({
		"name":     name,
		"domain":   domain,
		"password": args.password,
	}), headers={'content-type':'application/json'}).json()
	print_result(res)

def show(args):
	res = requests.get(args.server + 'mail/account/' + args.email + '/').json()
	print_result(res)
	
def list(args):
	res = requests.get(args.server + 'mail/account/', params = {
		'page_size': 10000,
		'domain': args.domain
	}).json()
	
	keys = ['id', 'submission_disabled', 'spoofing_whitelist']
	row_format	= "{:>48} {:>2} {:<60}"
	print(row_format.format(*keys))
	for row in res['results']:
		print(row_format.format(*[row[k] for k in keys]))
	pass

def set_password(args):
	url = args.server + 'mail/account/' + args.email + '/set_password/'
	res = requests.post(url, data=json.dumps({
		"password": args.password,
	}), headers={'content-type':'application/json'}).json()
	print_result(res)

def disable_submission(args):
	url = args.server + 'mail/account/' + args.email + '/disable_submission/'
	res = requests.post(url).json()
	print_result(res)

def enable_submission(args):
	url = args.server + 'mail/account/' + args.email + '/enable_submission/'
	res = requests.post(url).json()
	print_result(res)

def set_spoofing_whitelist(args):
	url = args.server + 'mail/account/' + args.email + '/set_spoofing_whitelist/'
	res = requests.post(url, data=json.dumps({
		"spoofing_whitelist": args.spoofing_whitelist,
	}), headers={'content-type':'application/json'}).json()
	print_result(res)

def delete(args):
	res = requests.delete(args.server + 'mail/account/' + args.email + '/')
	print(res.status_code)
	
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--server', '-s', action="store", help='API-Server [http://localhost:8000/]', default='http://localhost:8000/')
	subparsers = parser.add_subparsers(help='commands', dest='cmd')
	subparsers.required = True

	# create
	create_parser = subparsers.add_parser('create', help='Create new Mail Account')
	create_parser.add_argument('email',	   action='store', help='Email address')
	create_parser.add_argument('password', action='store', help='Password')
	create_parser.set_defaults(func=create)

	# show
	show_parser = subparsers.add_parser('show', help='Show Mail Account details')
	show_parser.add_argument('email', action='store', help='Email address')
	show_parser.set_defaults(func=show)

	# list
	list_parser = subparsers.add_parser('list', help='List all count-jobs')
	list_parser.add_argument('--domain', '-d', action='store', help='Domain')
	list_parser.set_defaults(func=list)
	
	# set_password
	set_password_parser = subparsers.add_parser('set_password', help='Set Password')
	set_password_parser.add_argument('email',	  action='store', help='Email address')
	set_password_parser.add_argument('password', action='store', help='Password')
	set_password_parser.set_defaults(func=set_password)
	
	# disable_submission
	disable_submission_parser = subparsers.add_parser('disable_submission', help='Disable Submission')
	disable_submission_parser.add_argument('email', action='store', help='Email address')
	disable_submission_parser.set_defaults(func=disable_submission)

	# enable_submission
	enable_submission_parser = subparsers.add_parser('enable_submission', help='Enable Submission')
	enable_submission_parser.add_argument('email', action='store', help='Email address')
	enable_submission_parser.set_defaults(func=enable_submission)

	# set_spoofing_whitelist
	set_spoofing_whitelist_parser = subparsers.add_parser('set_spoofing_whitelist', help='Set Spoofing Whitelist')
	set_spoofing_whitelist_parser.add_argument('email', action='store', help='Email address')
	set_spoofing_whitelist_parser.add_argument('spoofing_whitelist', action='store', help='Spoofing Whitelist')
	set_spoofing_whitelist_parser.set_defaults(func=set_spoofing_whitelist)

	# delete
	delete_parser = subparsers.add_parser('delete', help='Delete Mail Account')
	delete_parser.add_argument('email', action='store', help='Email address')
	delete_parser.set_defaults(func=delete)

	return parser.parse_args()

def main():
	args = parse_args()
	args.func(args)

if __name__ == '__main__':
	main()