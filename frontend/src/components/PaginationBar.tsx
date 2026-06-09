type PaginationBarProps = {
  page: number
  hasNextPage: boolean
  isLoading: boolean
  onPrevious: () => void
  onNext: () => void
}

export function PaginationBar({
  page,
  hasNextPage,
  isLoading,
  onPrevious,
  onNext,
}: PaginationBarProps) {
  return (
    <div className="pagination-bar">
      <button
        className="ghost-button"
        type="button"
        disabled={page === 0 || isLoading}
        onClick={onPrevious}
      >
        Previous
      </button>
      <span>Page {page + 1}</span>
      <button
        className="ghost-button"
        type="button"
        disabled={!hasNextPage || isLoading}
        onClick={onNext}
      >
        Next
      </button>
    </div>
  )
}
