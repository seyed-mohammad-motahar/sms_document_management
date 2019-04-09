# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
try:
    # python2
    from urlparse import urlparse
except:
    # python3
    from urllib.parse import urlparse


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_attachment = fields.Binary('Question attachment')
    type = fields.Selection([
        ('free_text', 'Multiple Lines Text Box'),
        ('textbox', 'Single Line Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('date', 'Date'),
        ('upload_file', 'Upload file'),
        ('simple_choice', 'Multiple choice: only one answer'),
        ('multiple_choice', 'Multiple choice: multiple answers allowed'),
        ('matrix', 'Matrix'),
        ('link', 'Link')],
        string='Type of Question', default='free_text', required=True)
    url_link = fields.Char(string='URL')

    @api.multi
    def validate_upload_file(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        answer = post[answer_tag]
        # Empty answer to mandatory question
        if self.constr_mandatory and not answer:
            errors.update({answer_tag: self.constr_error_msg})
        return errors

    @api.multi
    @api.constrains('url_link')
    def validate_url(self):
        for question in self:
            if all([question.type == 'link', question.url_link]):
                valid = False
                try:
                    result = urlparse(question.url_link)
                    valid = all([
                        result.scheme, result.netloc, result.path])
                except:
                    pass
                if not valid:
                    raise ValidationError(
                        'The URL of the question [%s] is invalid. '
                        'Please check!' % question.question)