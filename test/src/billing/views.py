from django.shortcuts import render, render_to_response
from django.conf import settings
from billing.forms import DaysAddForm
from billing.models import PriceToDays, Transaction
from mixins.mixins import LoginRequiredMixin
from users.models import PUser
from django.views.generic import TemplateView, View, FormView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
import datetime
import pytz
# Create your views here.
from django.urls import reverse
from django.contrib import messages
import stripe
from django.template.context_processors import csrf
from polls.models import PollItem

import random
import string


        # allowed_chars = ''.join((string.ascii_letters, string.digits))
        # unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))
        # print (unique_id)



stripe.api_key = settings.STRIPE_SECRET





# #This register script is only available if the user is not subscribed on stripe
# def register(request):
# 	form = CustomUserForm(request.POST)

# 	if request.method == 'POST':

# 		if form.is_valid():

# 			try:
# 				customer = stripe.Charge.create(
# 						amount = 2099,
# 						currency = "USD",
# 						description = form.cleaned_data['email'],
# 						card = form.cleaned_data['stripe_id'],#represents the token sent my stripe to acknowledge the transaction - starts with tok
# 					)
# 				# form.save()
# 				return redirect('Home') #successful credit card transaction

# 				# redirect('/register_sucess')

# 			# except stripe.CardError, e:
# 			except stripe.CardError:
# 				print ("there is an error here, your credit card has been declined")
# 				# form.add_error("This card has been declined")

# 				args = {}
# 				args.update(csrf(request))
# 				args['form'] = form
# 				args['publishable'] = settings.STRIPE_PUBLISHABLE
# 				args['months'] = range(1,12)
# 				args['years'] = range(2011,2036)
# 				args['soon'] = datetime.date.today() + datetime.timedelta(days=30)

# 			return HttpResponseRedirect('register.html', args)

# 	else:
# 		form = CustomUserForm()

# 		args = {}
# 		args.update(csrf(request))
# 		args['form'] = form
# 		args['publishable'] = settings.STRIPE_PUBLISHABLE
# 		args['months'] = range(1,12)
# 		args['years'] = range(2011,2036)
# 		args['soon'] = datetime.date.today() + datetime.timedelta(days=30)

# 		return render_to_response('register.html', args)





class SelectPlan(LoginRequiredMixin, TemplateView):
	template_name = "select_sub_plan.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SelectPlan, self).get_context_data(*args, **kwargs)

		Plan02 = get_object_or_404(PriceToDays, subplan="Plan02")
		Plan03 = get_object_or_404(PriceToDays, subplan="Plan03")
		Plan05 = get_object_or_404(PriceToDays, subplan="Plan05")

		# totaltipcount = (PollItem.objects.filter(allowed=True).count())*30

		#Price per month
		context['Plan02price'] = round(Plan02.cashprice/Plan02.daystoadd*30,2)
		context['Plan03price'] = round(Plan03.cashprice/Plan03.daystoadd*30,2)
		context['Plan05price'] = round(Plan05.cashprice/Plan05.daystoadd*30,2)

		# #Price per tip
		# context['Plan02pricepertip'] = round(context['Plan02price']/totaltipcount,4)
		# context['Plan03pricepertip'] = round(context['Plan03price']/totaltipcount,4)
		# context['Plan05pricepertip'] = round(context['Plan05price']/totaltipcount,4)

		# # numbers of days
		# context['Plan02days'] = Plan02.daystoadd
		# context['Plan03days'] = Plan03.daystoadd
		# context['Plan05days'] = Plan05.daystoadd
		
		# cashprice of the package
		context['Plan02total'] = Plan02.cashprice
		context['Plan03total'] = Plan03.cashprice
		context['Plan05total'] = Plan05.cashprice

		#name of the submission button
		context['Plan02'] = Plan02.subplan
		context['Plan03'] = Plan03.subplan
		context['Plan05'] = Plan05.subplan

		# Name of the plan
		context['Plan02subplan'] = Plan02.label
		context['Plan03subplan'] = Plan03.label
		context['Plan05subplan'] = Plan05.label

		return context

	def post(self, request, *args, **kwargs):
		# retrieving the sub subscription plan type
		# subtype_id = self.request.session.get("subtype_id")
		# subtypeobj = get_object_or_404(PriceToDays, label=subtype)

		if request.method == 'POST':
			subtype_id = request.POST.get('Plan')
			subtypeobj = get_object_or_404(PriceToDays, subplan=subtype_id)
			#save session for the credit package selected
			self.request.session["subtype_id"] = subtypeobj.id

			return redirect('StripeCheckOut')
		






# old for backup
# class SelectPlan(LoginRequiredMixin, TemplateView, FormView):
# 	template_name = "select_sub_plan.html"
# 	form_class = DaysAddForm

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(SelectPlan, self).get_context_data(*args, **kwargs)

# 		return context

# 	def form_valid(self, form):

# 		subtype = form.cleaned_data.get("subtype")
# 		subtypeobj = get_object_or_404(PriceToDays, label=subtype)
# 		#save session for the credit package selected
# 		self.request.session["subtype_id"] = subtypeobj.id

# 		return redirect('StripeCheckOut')

# 		# return super(SelectPlan, self).form_valid(form)












class StripeCheckOut(LoginRequiredMixin, TemplateView):
	template_name = "stripecheckout.html"
	success_url = '/'


	def dispatch(self, *args, **kwargs):
		dispatch = super(StripeCheckOut, self).dispatch(*args, **kwargs)

		#if credit package id is not selected to exit
		try:
			subtype_id = self.request.session.get("subtype_id")
		except:
			return reverse('Home')
		return dispatch


	def get_context_data(self, *args, **kwargs):
		context = super(StripeCheckOut, self).get_context_data(*args, **kwargs)

		subtype_id = self.request.session.get("subtype_id")
		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)
		context['subtype'] = subtypeobj
		context['price'] = subtypeobj.cashprice * 100
		context['pricen'] = subtypeobj.cashprice
		context['daysn'] = subtypeobj.daystoadd

		context.update(csrf(self.request))
		context['publishable'] = settings.STRIPE_PUBLISHABLE
		# context['months'] = range(1,13)
		# context['years'] = range(2011,2036)
		# context['soon'] = datetime.date.today() + datetime.timedelta(days=30)
		return context



	def post(self, request, *args, **kwargs):
		# retrieving the sub subscription plan type
		subtype_id = self.request.session.get("subtype_id")
		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)

		userobj = PUser.objects.get(user=self.request.user)
		token = request.POST.get("stripeToken")

		charge_amt = int(subtypeobj.cashprice * 100) #convert to integer - required by stripe
		adddays = subtypeobj.daystoadd

		startdate = datetime.date.today()
		tdelta = datetime.timedelta(days=adddays)
		enddate = startdate + tdelta

		try:
			customer = stripe.Charge.create(
					amount = charge_amt,
					currency = "USD",
					source=token,
					description = 'Charge - ' + str(userobj) + " " + str(subtypeobj.label),
				)
		except:

			messages.info(self.request, "This card has been declined.")
			return redirect('StripeCheckOut')


		plantype = subtypeobj.label

		print (plantype[:5])

		if plantype[:5] == "Basic":
			#membersubscription
			userobj.member = True
			userobj.substartdate = startdate
			userobj.subenddate = enddate
			userobj.memberp = False
			userobj.substartdatep = None
			userobj.subenddatep = None
		else:
			#pmembersubscription
			userobj.member = False
			userobj.substartdate = None
			userobj.subenddate = None
			userobj.memberp = True
			userobj.substartdatep = startdate
			userobj.subenddatep = enddate

		userobj.email = customer.source.name
		userobj.invoiceno = customer.id #Both are the same - for subscription I am using customer.invoice_prefix
		userobj.stripe_id = customer.id
		userobj.plan = adddays
		userobj.save()


		# record transaction here
		trans_obj = Transaction.objects.create(
			user=self.request.user,
			price=subtypeobj.cashprice,
			transaction_id=customer.id,
			startdate=startdate,
			enddate=enddate,
			description='Charge - ' + str(userobj) + " " + str(subtypeobj.label)
			)

		trans_obj.save()

		messages.success(self.request, "Thank you for you subscription.")
		
		return redirect("SuccessSub")





class SuccessSub(LoginRequiredMixin, TemplateView):
	template_name = "success_sub.html"


	def dispatch(self, *args, **kwargs):
		dispatch = super(SuccessSub, self).dispatch(*args, **kwargs)

		#if credit package id is not selected to exit
		try:
			subtype_id = self.request.session.get("subtype_id")
		except:
			return reverse('Home')
		return dispatch


	def get_context_data(self, *args, **kwargs):
		context = super(SuccessSub, self).get_context_data(*args, **kwargs)

		subtype_id = self.request.session.get("subtype_id")
		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)
		context['subtype'] = subtypeobj.label
		
		#membersubscription
		user = self.request.user
		context['name'] = user
		context['price'] = "%.2f" % round(subtypeobj.cashprice,2)
		context['email'] = PUser.objects.get(user=user).email
		context['invoiceno'] = PUser.objects.get(user=user).invoiceno

		#if premium then use premium dates of basic check for basic dates
		try:
			context['startdate'] = PUser.objects.get(user=user).substartdatep.date()
			context['enddate'] = PUser.objects.get(user=user).subenddatep.date()
		except:
			context['startdate'] = PUser.objects.get(user=user).substartdate.date()
			context['enddate'] = PUser.objects.get(user=user).subenddate.date()

		return context	












# class Subscribe1(LoginRequiredMixin, TemplateView, FormView):
# 	template_name = "subscribe1.html"
# 	form_class = CustomUserForm
# 	success_url = '/'

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(Subscribe1, self).dispatch(*args, **kwargs)
# 		try:
# 			subtype_id = self.request.session.get("subtype_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(Subscribe1, self).get_context_data(*args, **kwargs)

# 		subtype_id = self.request.session.get("subtype_id")
# 		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)
# 		context['subtype'] = subtypeobj
# 		context['price'] = subtypeobj.cashprice * 100
# 		context['pricen'] = subtypeobj.cashprice
# 		context.update(csrf(self.request))
# 		context['publishable'] = settings.STRIPE_PUBLISHABLE
# 		# context['months'] = range(1,13)
# 		# context['years'] = range(2011,2036)
# 		# context['soon'] = datetime.date.today() + datetime.timedelta(days=30)

# 		return context

# 	def form_valid(self, form):


# 		# retrieving the sub subscription plan type
# 		subtype_id = self.request.session.get("subtype_id")
# 		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)

# 		userobj = PUser.objects.get(user=self.request.user)

# 		print (form.cleaned_data)

# 		# userobj.stripe_id = form.cleaned_data.get('stripe_id')
# 		# stripe_id = form.cleaned_data.get('stripe_id')
# 		token = request.POST.get("stripeToken")



# 		print (token)

# 		charge_amt = subtypeobj.cashprice * 100
# 		adddays = subtypeobj.daystoadd

# 		startdate = datetime.date.today()
# 		tdelta = datetime.timedelta(days=adddays)
# 		enddate = startdate + tdelta



# 		customer = stripe.Charge.create(
# 				amount = charge_amt,
# 				currency = "USD",
# 				# customer = "testing",
# 				source=token,
# 				description = 'Charge - ' + str(userobj),
# 				# email = self.request.user.email, #this either has to be the email that the user is using to log in or his email updated under puser - for subscription
# 				# plan = subtypeobj.subplan, #represents the stripe plan that you set up on stripe.com - needs to match - for subscription
# 				# card = stripe_id,#represents the customer stripe id starts with cus
# 			)



# 		userobj.member = True
# 		# userobj.email = self.request.user.email
# 		userobj.substartdate = startdate
# 		userobj.subenddate = enddate

# 		userobj.invoiceno = customer.id #Both are the same - for subscription I am using customer.invoice_prefix
# 		userobj.stripe_id = customer.id
# 		userobj.plan = adddays
# 		userobj.save()

# 		messages.success(self.request, "Thank you for you subscription.")

# 		return redirect('SuccessSub')


# 		# try:
# 		# 	# retrieving the sub subscription plan type
# 		# 	subtype_id = self.request.session.get("subtype_id")
# 		# 	subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)

# 		# 	userobj = PUser.objects.get(user=self.request.user)

# 		# 	# userobj.stripe_id = form.cleaned_data.get('stripe_id')
# 		# 	# stripe_id = form.cleaned_data.get('stripe_id')

# 		# 	charge_amt = subtypeobj.cashprice * 100
# 		# 	adddays = subtypeobj.daystoadd

# 		# 	startdate = datetime.date.today()
# 		# 	tdelta = datetime.timedelta(days=adddays)
# 		# 	enddate = startdate + tdelta

# 		# 	customer = stripe.Charge.create(
# 		# 			amount = charge_amt,
# 		# 			currency = "USD",
# 		# 			# customer = "testing",
# 		# 			source="tok_visa",
# 		# 			description = 'Charge - ' + str(userobj),
# 		# 			# email = self.request.user.email, #this either has to be the email that the user is using to log in or his email updated under puser - for subscription
# 		# 			# plan = subtypeobj.subplan, #represents the stripe plan that you set up on stripe.com - needs to match - for subscription
# 		# 			# card = stripe_id,#represents the customer stripe id starts with cus
# 		# 		)


# 		# 	userobj.member = True
# 		# 	# userobj.email = self.request.user.email
# 		# 	userobj.substartdate = startdate
# 		# 	userobj.subenddate = enddate

# 		# 	userobj.invoiceno = customer.id #Both are the same - for subscription I am using customer.invoice_prefix
# 		# 	userobj.stripe_id = customer.id
# 		# 	userobj.plan = adddays
# 		# 	userobj.save()

# 		# 	messages.success(self.request, "Thank you for you subscription.")

# 		# 	return redirect('SuccessSub')

# 		# except:

# 		# 	messages.info(self.request, "This card has been declined.")
# 		# 	# form.add_error("This card has been declined")
# 		# 	#redirect to a page that prompts an error

# 		# return redirect('Subscribe1')







# class Subscribe(LoginRequiredMixin, TemplateView, FormView):

# 	template_name = "subscribe.html"
# 	form_class = CustomUserForm
# 	success_url = '/'

# 	#insert if subscribed already to exit

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(Subscribe, self).dispatch(*args, **kwargs)

# 		#if the user is subscribed
# 		# if self.request.user.puser.plan:
# 		# 	return redirect('Home')

# 		#if credit package id is not selected to exit
# 		try:
# 			subtype_id = self.request.session.get("subtype_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch


# 	def get_context_data(self, *args, **kwargs):
# 		context = super(Subscribe, self).get_context_data(*args, **kwargs)

# 		subtype_id = self.request.session.get("subtype_id")
# 		subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)
# 		context['subtype'] = subtypeobj
# 		context['price'] = "%.2f" % round(subtypeobj.cashprice,2)

# 		context.update(csrf(self.request))
# 		context['publishable'] = settings.STRIPE_PUBLISHABLE
# 		context['months'] = range(1,13)
# 		context['years'] = range(2011,2036)
# 		context['soon'] = datetime.date.today() + datetime.timedelta(days=30)

# 		return context

# 	def form_valid(self, form):

# 		try:
# 			# retrieving the sub subscription plan type
# 			subtype_id = self.request.session.get("subtype_id")
# 			subtypeobj = get_object_or_404(PriceToDays, id=subtype_id)


# 			userobj = PUser.objects.get(user=self.request.user)
# 			userobj.stripe_id = form.cleaned_data.get('stripe_id')
# 			stripe_id = form.cleaned_data.get('stripe_id')
# 			charge_amt = subtypeobj.cashprice * 100
# 			adddays = subtypeobj.daystoadd

# 			startdate = datetime.date.today()
# 			tdelta = datetime.timedelta(days=adddays)
# 			enddate = startdate + tdelta


# 			# user = form.save()
# 			#asking stripe to sub a customer a plan/ time to get paid nigga!!
# 			customer = stripe.Charge.create(

# 					amount = charge_amt,
# 					currency = "USD",	
# 					description = 'Subscription charge on voterable.com',
# 					# email = self.request.user.email, #this either has to be the email that the user is using to log in or his email updated under puser - for subscription
# 					# plan = subtypeobj.subplan, #represents the stripe plan that you set up on stripe.com - needs to match - for subscription
# 					card = userobj.stripe_id,#represents the customer stripe id starts with cus
# 				)

# 			userobj.member = True
# 			# userobj.email = self.request.user.email
# 			userobj.substartdate = startdate
# 			userobj.subenddate = enddate

# 			userobj.invoiceno = customer.id #Both are the same - for subscription I am using customer.invoice_prefix
# 			userobj.stripe_id = customer.id
# 			userobj.plan = adddays
# 			userobj.save()

# 			messages.success(self.request, "Thank you for you subscription.")

# 			#insert the subscribe button onto the home page and test it to see what happens when unsubscribed

# 			return redirect('SuccessSub')

# 		except:

# 			messages.info(self.request, "This card has been declined.")
# 			# form.add_error("This card has been declined")
# 			#redirect to a page that prompts an error

# 		return redirect('Subscribe')









class ConfirmCancel(LoginRequiredMixin, TemplateView):
	template_name = "cfncancel_sub.html"

	def dispatch(self, *args, **kwargs):
		dispatch = super(ConfirmCancel, self).dispatch(*args, **kwargs)

		# if the user is not subscribed
		if not self.request.user.puser.plan:
			return redirect('Home')
		return dispatch





def CancelSubscribe(request):

	customer = stripe.Customer.retrieve(request.user.puser.stripe_id)

	try:
		customer = stripe.Customer.retrieve(request.user.puser.stripe_id)
		customer.cancel_subscription(at_period_end=True)

		planid_cancel_obj = PUser.objects.get(user=request.user)
		planid_cancel_obj.plan = None
		planid_cancel_obj.stripe_id = None
		planid_cancel_obj.save()

		messages.success(request, "You subscription has been cancelled")

	# except Exception, e:
	# 	messages.error(request, e)

	except:
		messages.info(request, "Cancellation issue. Please contact the admin")


	return redirect("Home")
































# class StripeAddDays(LoginRequiredMixin, FormView):
# 	template_name = 'stripeaddcredits.html'
# 	form_class = DaysAddForm

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripeAddDays, self).get_context_data(*args, **kwargs)

# 		#insert puser model memberdate
# 		usersubdate = self.request.user.puser.memberdate
# 		utc=pytz.UTC
# 		nowdate = datetime.datetime.now().replace(tzinfo=utc)
# 		# tdelta = datetime.timedelta(days=30)
# 		# nowdate = nowdate - tdelta

# 		# tdelta = datetime.timedelta(days=30)
# 		# startdate = enddate - tdelta
# 		# startdate = startdate.date()

# 		if usersubdate <= nowdate:
# 			context["usersubdate"] = usersubdate
# 		return context

# 	def form_valid(self, form):

# 		subtype = form.cleaned_data.get("subtype")
# 		subtypeobj = get_object_or_404(PriceToDays, label=subtype)
# 		#save session for the credit package selected
# 		self.request.session["subtype_id"] = subtypeobj.id

# 		return super(StripeAddDays, self).form_valid(form)

# 	def get_success_url(self):
# 		return reverse('StripePayment')


# class StripePayment(LoginRequiredMixin, TemplateView):
# 	template_name = 'stripepayment.html'

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(StripePayment, self).dispatch(*args, **kwargs)
# 		#if credit package id is not selected to exit
# 		try:
# 			subtype_id = self.request.session.get("subtype_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripePayment, self).get_context_data(*args, **kwargs)
# 		subtype_id = self.request.session.get("subtype_id")
# 		price_pack = get_object_or_404(PriceToDays, id=subtype_id)

# 		#convert dollars into cents for stripe to use
# 		context["creditcostcents"] = price_pack.cashprice * 100
# 		context["creditcostdollars"] = price_pack.cashprice

# 		context["description"] = "Payment for " + str(price_pack.cashprice)

# 		context["credit"] = price_pack.daystoadd
# 		# context["stripe_key"] = settings.STRIPE_PUBLIC_KEY

# 		return context




# class StripeCheckOut(LoginRequiredMixin, TemplateView):

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(StripeCheckOut, self).dispatch(*args, **kwargs)
# 		#if credit package id is not selected to exit
# 		try:
# 			subtype_id = self.request.session.get("subtype_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch

# 	def post(self, request, *args, **kwargs):

# 		try:
# 			subtype_id = self.request.session.get("subtype_id")
# 			price_pack = get_object_or_404(PriceToDays, id=subtype_id)
# 			#convert dollars into cents for stripe to use
# 			cash = price_pack.cashprice * 100
# 			days = price_pack.daystoadd
# 		except:
# 			return reverse('Home')

# 		token = request.POST.get("stripeToken")

# 		description = "user " + str(self.request.user) + " paid for " + str(days) + " of credits"

# 		try:
# 			charge  = stripe.Charge.create(
# 			    amount      = cash,
# 			    currency    = "sgd",
# 			    source      = token,
# 			    description = description
# 			)

# 		except stripe.error.CardError as ce:
# 			return False, ce

# 		#might not need this else here?
# 		else:
# 			self.request.session["transaction_id"] = charge.id
# 			transaction = Transaction.objects.get_or_create(
# 				user=self.request.user,
# 				transaction_id=charge.id,
# 				success=True
# 				)[0]

# 			#saving the transaction as a record
# 			transaction.price=self.get_credit_cost()
# 			transaction.credit=self.get_credit()
# 			transaction.beforecredit=self.get_user_cred()
# 			transaction.aftercredit=int(self.get_user_cred()) + int(self.get_credit())
# 			transaction.save()
# 			#adding the credits to the account that the user has purchased
# 			credit = UserCredit.objects.get_or_create(
# 				user=self.request.user,
# 				)[0]

# 			credit.credit = int(self.get_user_cred()) + int(self.get_credit())
# 			credit.save()

# 			messages.success(request, "Thank you for your order. Please print this page.")
			
# 			return redirect("StripeInvoice")
# 	        # The payment was successfully processed, the user's card was charged.
# 	        # You can now redirect the user to another page or whatever you want



# class StripeInvoice(LoginRequiredMixin, TemplateView):
# 	template_name = 'invoice.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripeInvoice, self).get_context_data(*args, **kwargs)
# 		if self.request.user.is_authenticated():
# 			#retrieving contents of the transaction that the user has purchased
# 			context["user"] = self.get_transaction().user
# 			context["transaction_id"] = self.get_transaction().transaction_id
# 			context["price"] = self.get_transaction().price
# 			context["creditpurchased"] = self.get_transaction().credit
# 			context["currentcredit"] = self.get_transaction().aftercredit
# 			context["timestamp"] = self.get_transaction().timestamp
# 			messages.success(self.request, "You have succcessfully purchased " + str(self.get_transaction().credit) + " credits")
# 			del self.request.session["credit_id"]
# 			del self.request.session["transaction_id"]

# 		elif not self.request.user.is_authenticated():
# 			return Http404

# 		return context




























# class StripeAddCredits(LoginRequiredMixin, GetCheckoutMixin, FormView):
# 	template_name = 'stripeaddcredits.html'
# 	form_class = CreditForm

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripeAddCredits, self).get_context_data(*args, **kwargs)
# 		context["usercred"] = self.get_user_cred()
# 		return context

# 	def form_valid(self, form):
# 		credit = form.cleaned_data.get("credit")
# 		credit_pack = get_object_or_404(CreditToCash, label=credit)
# 		#save session for the credit package selected
# 		self.request.session["credit_id"] = credit_pack.id
# 		return super(StripeAddCredits, self).form_valid(form)

# 	def get_success_url(self):
# 		return reverse('StripePayment')


# class StripePayment(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
# 	template_name = 'stripepayment.html'

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(StripePayment, self).dispatch(*args, **kwargs)
# 		#if credit package id is not selected to exit
# 		try:
# 			credit_id = self.request.session.get("credit_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripePayment, self).get_context_data(*args, **kwargs)
# 		credit_id = self.request.session.get("credit_id")
# 		credit_pack = get_object_or_404(CreditToCash, id=credit_id)
# 		#convert dollars into cents for stripe to use
# 		context["creditcostcents"] = credit_pack.cashprice * 100
# 		context["creditcostdollars"] = credit_pack.cashprice

# 		context["description"] = "Payment for " + str(credit_pack.cashprice)

# 		context["credit"] = credit_pack.credits
# 		context["stripe_key"] = settings.STRIPE_PUBLIC_KEY

# 		return context




# class StripeCheckOut(LoginRequiredMixin, GetCheckoutMixin, TemplateView):

# 	def dispatch(self, *args, **kwargs):
# 		dispatch = super(StripeCheckOut, self).dispatch(*args, **kwargs)
# 		#if credit package id is not selected to exit
# 		try:
# 			credit_id = self.request.session.get("credit_id")
# 		except:
# 			return reverse('Home')
# 		return dispatch

# 	def post(self, request, *args, **kwargs):

# 		try:
# 			credit_id = self.request.session.get("credit_id")
# 			credit_pack = get_object_or_404(CreditToCash, id=credit_id)
# 			#convert dollars into cents for stripe to use
# 			cash = credit_pack.cashprice * 100
# 			credit = credit_pack.credits
# 		except:
# 			return reverse('Home')

# 		token = request.POST.get("stripeToken")

# 		description = "user " + str(self.request.user) + " paid for " + str(credit) + " of credits"

# 		try:
# 			charge  = stripe.Charge.create(
# 			    amount      = cash,
# 			    currency    = "sgd",
# 			    source      = token,
# 			    description = description
# 			)

# 		except stripe.error.CardError as ce:
# 			return False, ce

# 		else:
# 			self.request.session["transaction_id"] = charge.id
# 			transaction = Transaction.objects.get_or_create(
# 				user=self.request.user,
# 				transaction_id=charge.id,
# 				success=True
# 				)[0]

# 			#saving the transaction as a record
# 			transaction.price=self.get_credit_cost()
# 			transaction.credit=self.get_credit()
# 			transaction.beforecredit=self.get_user_cred()
# 			transaction.aftercredit=int(self.get_user_cred()) + int(self.get_credit())
# 			transaction.save()
# 			#adding the credits to the account that the user has purchased
# 			credit = UserCredit.objects.get_or_create(
# 				user=self.request.user,
# 				)[0]

# 			credit.credit = int(self.get_user_cred()) + int(self.get_credit())
# 			credit.save()

# 			messages.success(request, "Thank you for your order. Please print this page.")
			
# 			return redirect("StripeInvoice")
# 	        # The payment was successfully processed, the user's card was charged.
# 	        # You can now redirect the user to another page or whatever you want



# class StripeInvoice(LoginRequiredMixin, GetCheckoutMixin, TemplateView):
# 	template_name = 'invoice.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(StripeInvoice, self).get_context_data(*args, **kwargs)
# 		if self.request.user.is_authenticated():
# 			#retrieving contents of the transaction that the user has purchased
# 			context["user"] = self.get_transaction().user
# 			context["transaction_id"] = self.get_transaction().transaction_id
# 			context["price"] = self.get_transaction().price
# 			context["creditpurchased"] = self.get_transaction().credit
# 			context["currentcredit"] = self.get_transaction().aftercredit
# 			context["timestamp"] = self.get_transaction().timestamp
# 			messages.success(self.request, "You have succcessfully purchased " + str(self.get_transaction().credit) + " credits")
# 			del self.request.session["credit_id"]
# 			del self.request.session["transaction_id"]

# 		elif not self.request.user.is_authenticated():
# 			return Http404

# 		return context
