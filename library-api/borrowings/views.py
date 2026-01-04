from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from books.models import Book
from members.models import Member

class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        member_id = request.data.get('member')

        try:
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
        except:
            return Response({"error": "Book or Member not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce available copies
        book.available_copies -= 1
        book.save()

        borrow_record = BorrowRecord.objects.create(book=book, member=member)
        serializer = self.get_serializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
