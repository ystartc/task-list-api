from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.is_complete
            }
    
    #returns all the attributes that must be passed in order to create a record. All not nullable instance variables accept id.'
    @classmethod
    def get_attributes(cls):
        return 'title', 'description'
    
    @classmethod
    def from_dict(cls, request_body):
        task = cls(
                title=request_body['title'],
                description=request_body['description'],
                is_complete=request_body.get('is_complete', False),
                completed_at=request_body.get('completed_at', None),
                goal_id=request_body.get('goal_id', None))
        return task
    
    ### temporal function: above to_dict and from_dict needs to be refactored and it dependecies fixed accordingly. no time rn...
    # @classmethod
    # def to_dict_with_goal_id(cls, request_body):
    #     if request_body['goal_id']:    
    #         return {
    #             'id': cls.id,
    #             'title': cls.title,
    #             'description': cls.description,
    #             'is_complete': cls.is_complete,
    #             'goal_id': cls.goal_id}
        
    @classmethod
    def from_dict_with_parent(cls, request_body, parent_id):
        task = cls(
                title=request_body['title'],
                description=request_body['description'],
                is_complete=request_body.get('is_complete', False),
                completed_at=request_body.get('completed_at', None),
                goal_id=parent_id)
        return task