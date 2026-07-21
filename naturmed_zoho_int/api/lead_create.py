import frappe
import requests


def clean(value):
    if value is None:
        return ""
    return str(value).replace("\xa0", "").strip()


def create_lead(doc, method=None):

    try:
        config = frappe.get_single("Zoho Configuration")

        token_url = config.token_url
        lead_url = config.lead_url

        token_response = requests.post(
            token_url,
                params={
                    "refresh_token": "1000.957330158b7c18c9c557a4eefd5315a1.c9b2c012d78e13bcd26b8c217ddcafe7",
                    "client_id": "1000.DLPRFKDWMPA9538R4OC2H4FEMT4MBN",
                    "client_secret": "6e1c4f56fc3ed1b80ca51dfc24f05b9048e2efc3c2",
                    "grant_type": "refresh_token"
                },
                timeout=30
            )



        token_response.raise_for_status()

        access_token = token_response.json().get("access_token")


        if not access_token:
            frappe.log_error(
                title="Zoho Lead Sync",
                message="Access token not found."
            )
            return

        payload = {
            "data": [
                {
                    "City": clean(doc.city),
                    "Country": clean(doc.country),
                    "Flat_House_No_Building_Apartment_Name": "",
                    "Latitude": "",
                    "Longitude": "",
                    "State": clean(doc.state),
                    "Street": "",
                    "Zip_Code": "",
                    "Annual_Revenue": doc.annual_revenue or 0,
                    "Connected_To__s": "",
                    "Customer_Group": clean(doc.customer_group),
                    "Customer_Priority": clean(doc.custom_customer_priority),
                    "Description": clean(doc.custom_about_the_company),
                    "Email": clean(doc.email_id),
                    "Fax": clean(doc.fax),
                    "Industry": clean(doc.industry),
                    "Last_Name": clean(doc.last_name) or clean(doc.name),
                    "Lead_Source": clean(doc.source),
                    "Lead_Status": clean(doc.status),
                    "Linkedin_URL_Lead_Contact_Detail": "",
                    "Mobile": clean(doc.mobile_no),
                    "First_Name": clean(doc.first_name),
                    #"Next_Contact_Date": str(doc.custom_next_contact_by) if doc.custom_next_contact_by else "",
                    "No_of_Employees": "300",      # client discussion pending
                    "Company": clean(doc.company_name),
                    "Phone": clean(doc.phone),
                    "Rating": "",
                    "Salutation": clean(doc.salutation),
                    "Designation": clean(doc.job_title),
                    "Secondary_Email": "",
                    "Skype_ID": "",
                    "Tag": "",
                    "To_Discuss": "",
                    "Twitter": "",
                    "Website": clean(doc.website)
                }
            ],
            "trigger": [
                "approval",
                "workflow",
                "blueprint"
            ]
        }


        response = requests.post(
            lead_url,
            headers={
                "Authorization": f"Zoho-oauthtoken {access_token}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )



        try:
            response_data = response.json()
        except Exception:
            response_data = response.text

        frappe.log_error(
            title="Zoho Lead Payload",
            message=frappe.as_json(payload, indent=2)
        )

        frappe.log_error(
            title="Zoho Lead Response",
            message=frappe.as_json(response_data, indent=2)
        )

    except Exception:
        frappe.log_error(
            title="Zoho Lead Sync Error",
            message=frappe.get_traceback()
        )