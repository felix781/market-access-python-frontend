from django import forms


class BarrierSource:
    """
    Source as in:
     - Where did you hear about the barrier?
     - Who told you about it?
    """
    COMPANY = "COMPANY"
    TRADE = "TRADE"
    GOVT = "GOVT"
    OTHER = "OTHER"

    @classmethod
    def choices(cls):
        return (
            (cls.COMPANY, "Company"),
            (cls.TRADE, "Trade association"),
            (cls.GOVT, "Government entity"),
            (cls.OTHER, "Other"),
        )


class RelatedToBrexit:
    YES = 1
    NO = 2
    DONT_KNOW = 3

    @classmethod
    def choices(cls):
        return (
            (cls.YES, "Yes"),
            (cls.NO, "No"),
            (cls.DONT_KNOW, "Don't know"),
        )


class NewReportBarrierAboutForm(forms.Form):
    BS = BarrierSource()
    barrier_title = forms.CharField(
        label="Name this barrier",
        help_text="Include the name of the product, "
                  "service or investment and the type of problem. "
                  "For example, Import quotas for steel rods."
    )
    product = forms.CharField(label="What product, service or investment is affected?",)
    source = forms.ChoiceField(
        label="Who told you about the barrier?",
        choices=BS.choices(),
    )
    other_source = forms.CharField(label="Please specify", required=False)
    eu_exit_related = forms.ChoiceField(
        label="Is this issue caused by or related to Brexit?",
        choices=RelatedToBrexit.choices(),
    )
